Here I will describe the process of creating a relayer between two cosmos networks
Rizon and Kichain to be exact
In my case they were on one server, so rizon ports needed to be changed

**First of all we need tockeck is this is at all possible ( it wasn't until kichain-t-4 =) )**

$ rizond q ibc-transfer params
receive_enabled: true
send_enabled: true

$ kid q ibc-transfer params
receive_enabled: true
send_enabled: true

Everything is in order and cross-transactions are available between these two networks

**1) We need to install a relayer**
https://github.com/cosmos/relayer

$ git clone git@github.com:cosmos/relayer.git
$ git checkout v0.9.3
$ cd relayer && make install

**2) We need to initialize it**

$ rly config init

**3) And create chain configurations**
In our particular case we will make a new directory and store those configurations there 

$ mkdir rly_config
$ cd rly_config

$ nano kichain_config.json
{
  "chain-id": "kichain-t-4",
  "rpc-addr": "http://127.0.0.1:26657",
  "account-prefix": "tki",
  "gas-adjustment": 1.5,
  "gas-prices": "0.025utki",
  "trusting-period": "48h"
}
$ nano rizon_config.json
{
  "chain-id": "groot-011",
  "rpc-addr": "http://127.0.0.1:26652",
  "account-prefix": "rizon",
  "gas-adjustment": 1.5,
  "gas-prices": "0.0001uatolo",
  "trusting-period": "48h"
}

**4) We will then add this to relayer config**
$ rly chains add -f kichain_config.json
$ rly chains add rizon_config.json

**5) Next step is creating new keys and addresses**

$ rly keys add kichain-t-4 wallet_name
$ rly keys add groot-011 wallet_name_2

Or we can restore them if previousl experemented in kichain-t-3

$ rly keys restore kichain-t-4 wallet_name “mnemonic”
$ rly keys restore groot-011 wallet_name_2 “mnemonic”

**6) Then we need to add these keys to relayer config**

$ rly chains edit kichaint-4 key wallet_name
$ rly chains edit groot-011 key wallet_name_2


**7) I personally received addresses in kichain and rizon network**
I used a faucet in rizon network to get some coins and transferred coins from my main kichain wallet to new one

We need to check the balances to make sure the funds are there

rly q balance kichain-t-4
rly q balance groot-011

**8) Next step is clients initializing for both networks**

$ rly light init kichain-t-4

successfully created light client for kichain-t-4 by trusting endpoint http://127.0.0.1:26657...

$ rly light init groot-011

successfully created light client for groot-011 by trusting endpoint http://127.0.0.1:26652…

**9) We create a channel between two networks**

$ rly paths generate kichain-t-4 groot-011 transfer --port=transfer

Generated path(transfer), run 'rly paths show transfer --yaml' to see details


**10) After that we can confirm in a config file that a new path has been created**

$ nano ~/.relayer/config/config.yaml 

global:
  api-listen-addr: :5183
  timeout: 10m
  light-cache-size: 20
chains:
- key: lagartos
  chain-id: kichain-t-4
  rpc-addr: http://127.0.0.1:26657
  account-prefix: tki
  gas-adjustment: 1.5
  gas-prices: 0.025utki
  trusting-period: 48h
- key: lagartos_2
  chain-id: groot-011
  rpc-addr: http://127.0.0.1:26652
  account-prefix: rizon
  gas-adjustment: 1.5
  gas-prices: 0.0001uatolo
  trusting-period: 48h
paths:
  transfer:
    src:
      chain-id: kichain-t-4
      client-id: 07-tendermint-51
      connection-id: connection-7
      channel-id: channel-50
      port-id: transfer
      order: UNORDERED
      version: ics20-1
    dst:
      chain-id: groot-011
      client-id: 07-tendermint-18
      connection-id: connection-17
      channel-id: channel-14
      port-id: transfer
      order: UNORDERED
      version: ics20-1
    strategy:
      type: naive

Here we can also change timeout params from
*timeout: 10s* 
to
*timeout: 10m* 

To be sure that our transactions will occur

**10) We shall check that pass** 

$ rly paths list

0: transfer             -> chns(✔) clnts(✔) conn(✔) chan(✔) (kichain-t-4:transfer<>groot-011:transfer)

We can see checkmarks – everything is good at this point


**11) We can also check if the chains are ready to relay over**

$ rly chains list

 0: kichain-t-4          -> key(✔) bal(✔) light(✔) path(✔)
 1: groot-011            -> key(✔) bal(✔) light(✔) path(✔)

Good to go


**12) We can transfer funds between out test wallets**

$ rly tx transfer groot-011 kichain-t-4 1000uatolo $(rly chains address kichain-t-4)

✔ [groot-011]@{418670} - msg(0:transfer) 

hash(0FA4A42C8FDCFA6CDB949947A7D463B36083FC5E55A876DE91DB3979641EEFBE)
https://testnet.mintscan.io/rizon/txs/0FA4A42C8FDCFA6CDB949947A7D463B36083FC5E55A876DE91DB3979641EEFBE



hash(C673AC5BC67C03AE8642CA7A8096E5BCF9F74E9B31162D86C09D7ABCAE02FBC7)
https://testnet.mintscan.io/rizon/txs/C673AC5BC67C03AE8642CA7A8096E5BCF9F74E9B31162D86C09D7ABCAE02FBC7

hash(7408603C90452C3AAFEF494F7EDFAD5406D44522EA4F1F05942A0F33ED5BA585)
https://testnet.mintscan.io/rizon/txs/7408603C90452C3AAFEF494F7EDFAD5406D44522EA4F1F05942A0F33ED5BA585

hash(4AEA97EACCA7CFF353C0050D566162F40463E416EB4EB10085E9A47C543456CA)
https://testnet.mintscan.io/rizon/txs/4AEA97EACCA7CFF353C0050D566162F40463E416EB4EB10085E9A47C543456CA

hash(F2D7B9B829C1214BFD736C8535EE64E8C3538C2AD5E5D6F75DEFB6CE07F77981)
https://testnet.mintscan.io/rizon/txs/F2D7B9B829C1214BFD736C8535EE64E8C3538C2AD5E5D6F75DEFB6CE07F77981


$ rly tx transfer kichain-t-4 groot-011  1000utki $(rly chains address groot-011)

✔ [kichain-t-4]@{220648} – msg(0:transfer)

hash(7C648BBBEE840795B39BA0CA6ED27F60D873A8822ECDB2F75C23D713EC26741D)
hash(FC47D8D36710EA56C6B8313CDEF4313E97B3D3EC7AA2B81EF36819B04B269D9F)
hash(5AA9904681DCA5B501D97F8F7C4B7ED21AF4082FC2ED4E1131A93DD6E17C2367)
hash(53BB632883236DCA2709CA123F8723C448019959F2FB8B358FDDDE2C60F65051)
hash(DD540C67BA90B1571181FE8964E3F553A8F688922B7A1E43543624B99A6BB858)

These are working quite nicely

**13) And after that we can transfer funds from our main wallets**

In ma case I have to use keyring-dir flag for kichain

We can find channes of the networks in path sections of the config file

$ nano ~/.relayer/config/config.yaml

paths:
  transfer:
    src:
      chain-id: kichain-t-4
      client-id: 07-tendermint-51
      connection-id: connection-7
      channel-id: channel-50
      port-id: transfer
      order: UNORDERED
      version: ics20-1
    dst:
      chain-id: groot-011
      client-id: 07-tendermint-18
      connection-id: connection-17
      channel-id: channel-14
      port-id: transfer
      order: UNORDERED
      version: ics20-1
    strategy:
      type: naive


$ kid tx ibc-transfer transfer transfer channel-50 rizon19hnej3ucqqls5wcn40cv00s9qvasgy38jvpnqu 1000utki --from kokorin9 --fees=5000utki --gas=auto --chain-id kichain-t-4 --home /root/testnet/kid --keyring-dir /root/.kid/

"txhash":"87CF2B9D4BFE3AE8084ADE6A3EDE6E509602539065F643E5211E037CE1E66A62"
"txhash":"CF527CF1DFB14F075C1E8B53B8F87541B10AE118F032CEB442A255AE3496E4C1

And node flag for rizon 

$ rizond tx ibc-transfer transfer transfer channel-14 tki1j0yvamr7vts0ka7zzl2fjc0k5k3srwssdl008p 1000uatolo --from kokorin9 --fees=5000uatolo --gas=auto --chain-id groot-011 --node "tcp://127.0.0.1:26652"

Everything went smoothly

txhash: 505BF0056EE932FFBC4DB9BCB5BB5168A7DEC26FB0E35F61BB4708BA29E194E2
txhash: 4A9BC1A34BEB6278F206B4F893CE8A5F99914284D80337E4B3E6940E321D7124

txhash: E6D1F8F98D9D86AA165529CA6EF569A3D0A6B65B208AF0CD4B7C598594EECFF2

txhash: 376B1622589DE70DB28F4F5C037CB38693A4F52EEFD10B100886BC1D48E20197
txhash: E688590FD449591837E38770695961947502F07DEA51196C0315BEAEC61A8D1D
txhash: 53CB374E353769B2867355DD6E80ABE891B57DF2FFC5BF26905DFA4FF17DE25D

**14) We can check balances again**

$ rly q balance kichain-t-4
8000transfer/channel-50/uatolo,214643utki

$ rly q balance groot-011
6000transfer/channel-14/utki,9994453uatolo

**15) Creating a service**

My kichain service is named kii

sudo tee /etc/systemd/system/rlyd.service > /dev/null <<EOF
[Unit]

Description=relayer client
After=network-online.target, kii.service

[Service]

User=root
ExecStart=$(which rly) start transfer
Restart=always
RestartSec=3
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
EOF

**16) After that we shall start a service file and check logs**

$ sudo systemctl daemon-reload <br/>
$ sudo systemctl enable rlyd <br/>
$ sudo systemctl start rlyd <br/> 
$ journalctl -u rlyd -f <br/>

Started relayer client.
I[2021-09-07|11:19:35.699] - listening to tx events from kichain-t-4...
rly[2780953]: I[2021-09-07|11:19:35.699] - listening to block events from kichain-t-4...
 rly[2780953]: I[2021-09-07|11:19:35.712] - listening to tx events from groot-011...
rly[2780953]: I[2021-09-07|11:19:35.716] - listening to block events from groot-011...
rly[2780953]: I[2021-09-07|11:19:36.418] - No packets to relay between [kichain-t-4]port{transfer} and [groot-011]port{transfer}
rly[2780953]: I[2021-09-07|11:19:38.890] • [kichain-t-4]@{229433} - actions(0:withdraw_delegator_reward,1:withdraw_delegator_reward,2:withdraw_delegator_reward,3:withdraw_delegator_reward) hash(69D9DED54B417730C8CCC333E7D8A8D9D7D35EA2EFB9803BB2D7291E55CF4581)

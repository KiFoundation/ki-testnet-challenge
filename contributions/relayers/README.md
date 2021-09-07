### edit config.toml on your two nodes for listening from the internet and restart service

change ```laddr = "tcp://127.0.0.1:26657"``` to ```laddr = "tcp://0.0.0.0:26657"```


Go to the server with the relayer

### download and install go


```
wget https://golang.org/dl/go1.17.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.17.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
go version
```

### download and install relayer
```
git clone https://github.com/cosmos/relayer.git
cd relayer
git checkout v0.9.3
make install

echo 'export PATH=$PATH:/root/go/bin' >> ~/.bashrc
source ~/.bashrc
```
### Initialize the relayer's configuration.
```
rly config init
```

### add config kichain
```
cd $HOME/relayer/configs
nano ki_config.json

{
  "chain-id": "kichain-t-4",
  "rpc-addr": "http://node_ip:26657",
  "account-prefix": "tki",
  "gas-adjustment": 1.5,
  "gas-prices": "0.025utki",
  "trusting-period": "48h"
}
```

### add config rizon
```
nano riz_config.json


{
  "chain-id": "groot-011",
  "rpc-addr": "http://node_ip:26657",
  "account-prefix": "rizon",
  "gas-adjustment": 1.5,
  "gas-prices": "0.025uatolo",
  "trusting-period": "48h"
}
```
```
Usage:
  rly chains add [flags]
```
```
rly chains add -f ki_config.json
rly chains add -f riz_config.json
```
### Either import or create new keys for the relayer to use when signing and relaying transactions
```
Usage:
  rly keys add [chain-id] [[name]] [flags]
  ```
```
rly keys add kichain-t-4 kif
rly keys add groot-011 rizon
```

or restore key
```
Usage:
  rly keys restore [chain-id] [name] [mnemonic] [flags]
```
```
rly keys restore kichain-t-4 kif "your mnemonic"
rly keys restore groot-011 rizon "your mnemonic"
```
### Assign the relayer chain-specific keys created or imported above to the specific chain's configuration. Note, key from step
```
Usage:
  rly chains edit [chain-id] [key] [value] [flags]
```

```
rly chains edit kichain-t-4 key kif
rly chains edit groot-011 key rizon
```
### Ensure both relayer accounts are funded by querying each.
```
Usage:
  rly query balance [chain-id] [[key-name]] [flags]
```
```
rly q balance kichain-t-4
rly q balance groot-011
```

### Now we are ready to initialize the light clients on each network. The relayer will used the configured RPC endpoints from each network to fetch header information and initialize the light clients.
```
Usage:
  rly light init [chain-id] [flags]
```

```
rly light init kichain-t-4 -f
rly light init groot-011 -f
```
### Next, we generate a new path representing a client, connection, channel and a specific port between the two networks.
```
rly paths generate kichain-t-4 groot-011 ibc --port=transfer
rly paths show ibc--yaml    to see details
```
### Open config relayer
```
nano ~/.relayer/config/config.yaml
```

### change section paths,add connection-id and channel-id
```
paths:
  ibc:
    src:
      chain-id: kichain-t-4
      client-id: 07-tendermint-8
      connection-id: connection-29
      channel-id: channel-56
      port-id: transfer
      order: UNORDERED
      version: ics20-1
    dst:
      chain-id: groot-011
      client-id: 07-tendermint-22
      connection-id: connection-4
      channel-id: channel-18
      port-id: transfer
      order: UNORDERED
      version: ics20-1
    strategy:
      type: naive
```
### run rly
```
rly start ibc
```
### if all ok,greate and run service

```
tee /etc/systemd/system/rlyd.service > /dev/null <<EOF
[Unit]
Description=relayer client
After=network-online.target, starsd.service
[Service]
User=$USER
ExecStart=$(which rly) start ibc
Restart=always
RestartSec=3
LimitNOFILE=65535
[Install]
WantedBy=multi-user.target
EOF
```
```
systemctl daemon-reload
systemctl enable rlyd
systemctl start rlyd
```
### To check the logs of a relay, use:
```
journalctl -u rlyd -f
```

### we conduct a transaction
```
Usage:
rly transact transfer [src-chain-id] [dst-chain-id] [amount] [dst-addr] [flags]
```
in my case, the command looks like this
```
rly tx transfer groot-011 kichain-t-4  1000000uatolo $(rly chains address kichain-t-4)
```
I[2021-09-06|19:14:29.799] ✔ [groot-011]@{419227} - msg(0:transfer) hash(CFD863755F210D4BDBAE5655112E6B0E9310B5AC0ECFD0D1532105884F64531D)

```
rly tx transfer kichain-t-4 groot-011 1000000utki $(rly chains address groot-011)
```

I[2021-09-06|19:14:01.786] ✔ [kichain-t-4]@{221200} - msg(0:transfer) hash(DE2B48A986C298DC90ADF5830E8B8624CF92BA998BFEFFF9F29A6C7876728170)

### go to the rizon server and run the command
```
Usage:
rizond tx ibc-transfer transfer [src-port] [src-channel] [receiver] [amount] [flags]
```

in my case, the command looks like this
```
rizond tx ibc-transfer transfer transfer channel-18 tki15h774756q3zxzv46y7k69t2prd6sam9muh4sqy "1000000uatolo" --from rizon --chain-id=groot-011 --fees="25uatolo" --gas=auto
```
HASH
```
2ED825F8731D819B382F3057E7D7142549A6828DC95E2E05458FD7EF01A51889
```
https://testnet.mintscan.io/rizon/txs/2ED825F8731D819B382F3057E7D7142549A6828DC95E2E05458FD7EF01A51889

### go to the kichain server and run the command

```
Usage:
kid tx ibc-transfer transfer [src-port] [src-channel] [receiver] [amount] [flags]
```
in my case, the command looks like this
```
kid tx ibc-transfer transfer transfer channel-56 rizon1h9s2gq7sslfn8k3836s35ve4m6kmr70l8f6vlk 1000000utki --from kif --fees=5000utki --gas=auto --chain-id kichain-t-4 --home $HOME/kif/kid
```
HASH
```
7AF3D215B964AA1EC3E9F35E00FAD045B229EB6CD30B22AFF0A56888433B26A3
```
https://api-challenge.blockchain.ki/txs/7AF3D215B964AA1EC3E9F35E00FAD045B229EB6CD30B22AFF0A56888433B26A3

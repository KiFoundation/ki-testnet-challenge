# IBC transactions Task for Kichain 

## This guide describes how to perform IBC transactions between Kichain and Umee networks
### Target: To launch a relayer with an existing IBC enabled chain in the Cosmos Ecosystem
Requirements : 
- Start a relayer 
- Perform multiple cross chain Txs 
- Publish technical documentations (Medium or Github Readme):
 - Used relayer client (Version, repo, …) 
- Installation instruction (specs and requirements) 
- Configurations (timeouts, paths, chains, … ) 
- Channels 
- Instructions to send a cross chain transaction 
- hash of the performed Transactions 
- Maintain the relayer until the end of the challenge

### Installation the repeater on Umee node server
>⚠️ Unless otherwise specified all subsequent steps are performed on Umee node server

Download and install go (if not installed)
```bash
wget https://golang.org/dl/go1.17.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.17.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
go version
```
Download and install relayer
```bash
git clone https://github.com/cosmos/relayer.git
cd relayer
make install
echo 'export PATH=$PATH:/root/go/bin' >> ~/.bashrc
source ~/.bashrc
```
Checking version
```bash
rly version
```
Output shoud be like:<br/>
`version: 1.0.0-rc1-152-g112205b`

Checking if our networks supports IBC. We need to check for both networks: Kichain and Umee
```bash
kid q ibc-transfer params #
```
Output shoud be like:<br/>
`receive_enabled: true`<br/>
`send_enabled: true`

Initialize the relayer's configuration:
```bash
rly config init
```

Creation settings file for KiChain network
```bash
cd ~
mkdir rly_config 
cd rly_config
nano kichain-t-4.json
```
Paste config below into the file
```bash
{ "chain-id": "kichain-t-4", "rpc-addr": "https://rpc-challenge.blockchain.ki:443", "account-prefix": "tki", "gas-adjustment": 1.5, "gas-prices": "0.025utki", "trusting-period": "48h" }
```
CTRL + O - save file <br/>
CTRL + X - close file

>We use he global RPC = `https://rpc-challenge.blockchain.ki:443` because KiChain client is on another server

Creation settings file for Umee network
```bash
nano umee-betanet-1.json
```
Paste config below into the file
```bash
{ "chain-id": "umee-betanet-1", "rpc-addr": "http://localhost:26657", "account-prefix": "umee", "gas-adjustment": 1.5, "gas-prices": "0.025uumee", "trusting-period": "48h" }
```
CTRL + O - save file <br/>
CTRL + X - close file

>We use he local RPC = `http://localhost:26657` because Umee client is local 

Adding settings to the Relayer configuration
```bash
rly chains add -f umee-betanet-1.json
rly chains add -f kichain-t-4.json
cd ~
```

### Creating new wallets
```bash
rly keys add umee-betanet-1 <YOUR_UMEE_WALLET_NAME>
rly keys add kichain-t-4 <YOUR_KICHAI_WALLET_NAME>
```
>⚠️ Save mnemonics for wallets!

>In the examples I will use the following wallets:<br/>
>Nane = `Miliwatt-rly-um`, address= `umee1ymx74ypkktunu59ks00jaw5cd66nwv0khzlgnr`<br/>
>Nane = `Miliwatt-rly-ki`, address= `tki1e7vtgqh63u8vll45jan98lxx72pfgs59wm9azx`

### Adding the generated keys to the Relayer configuration:
```bash
rly chains edit umee-betanet-1 key <YOUR_UMEE_WALLET_NAME>
rly chains edit kichain-t-4 key <YOUR_KICHAI_WALLET_NAME>
```

### Replenishment of created wallets 

Replenishment of Umee wallet
```bash
umeed tx bank send <FROM_existing_Umee_replenished_address> <TO_umee_address_relayer> <AMOUNT>uumee --chain-id="umee-betanet-1" -y
```
Replenishment of Kichain wallet
>⚠️ This step are performed on Kichain server
```bash
kid tx bank send <FROM_existing_Kichain_replenished_address> <TO_ki_address_relayer> <AMOUNT>utki --chain-id kichain-t-4 --gas=auto --fees=100utki --home $HOME/kichain/kid
```

Both wallets must have coins, check it out
```bash
rly q balance umee-betanet-1
rly q balance kichain-t-4
```

### Light client initialization for both networks
```bash
rly light init umee-betanet-1 -f
rly light init kichain-t-4 -f
```

Output shoud be like:<br/>
`successfully created light client for umee-betanet-1 by trusting endpoint http://localhost:26657...` <br/>
`successfully created light client for kichain-t-4 by trusting endpoint https://rpc-challenge.blockchain.ki:443...`

### Generating a channel between networks
```bash
rly paths generate umee-betanet-1 kichain-t-4 transfer --port=transfer
```

Output shoud be like: <br/>
`Generated path(transfer), run 'rly paths show transfer --yaml' to see details`

### Check chains
```bash
rly chains list
```

Output shoud be like:<br/>
`0: umee-betanet-1       -> key(✔) bal(✔) light(✔) path(✔)`<br/>
`1: kichain-t-4          -> key(✔) bal(✔) light(✔) path(✔)`

Check Path
```bash
rly paths show transfer
```

Output shoud be like:<br/>
`Path "transfer" strategy(naive):`<br/>
`  SRC(umee-betanet-1)`<br/>
`    ClientID:     07-tendermint-1`<br/>
`    ConnectionID: connection-1`<br/>
`    ChannelID:    channel-0`<br/>
`    PortID:       transfer`<br/>
`  DST(kichain-t-4)`<br/>
`    ClientID:     07-tendermint-13`<br/>
`    ConnectionID: connection-17`<br/>
`    ChannelID:    channel-61`<br/>
`    PortID:       transfer`<br/>
`  STATUS:`<br/>
`    Chains:       ✔`<br/>
`    Clients:      ✔`<br/>
`    Connection:   ✔`<br/>
`    Channel:      ✔`<br/>

### Performance cross-network transaction from Umee to KiChain on Umee node server

To check that the transaction has taken place, it will be convenient to check the current balances on the wallets 
```bash
rly q balance umee-betanet-1
rly q balance kichain-t-4
```
Template for transaction from Umee to KiChain network
```bash
rly transact transfer <source-chain> <destination-chain> <amount-token> <KiChain-destination-wallet-address> --path transfer
```

>An example for our wallet:<br/>
>`rly tx transfer umee-betanet-1 kichain-t-4 5000uumee tki1e7vtgqh63u8vll45jan98lxx72pfgs59wm9azx --path transfer`

Compare the balance on the wallets with the previous values
```bash
rly q balance umee-betanet-1
rly q balance kichain-t-4
```
>Hash details for a transaction through the Umiya network can be viewed on the following path in the explorer
>```
>https://explorer-umee.nodes.guru/transactions/<hash>
>```

### Performance cross-network transaction from KiChain to Umee on Umee node server
Template for transaction is the same
```bash
rly transact transfer <source-chain> <destination-chain> <amount-token> <Umee-destination-wallet-address> --path transfer
```
>An example for our wallet:<br/>
>`rly tx transfer kichain-t-4 umee-betanet-1 30000utki umee1ymx74ypkktunu59ks00jaw5cd66nwv0khzlgnr --path transfer`

Compare the balance on the wallets with the previous values
```bash
rly q balance umee-betanet-1
rly q balance kichain-t-4
```
>An example for our wallets: <br/>
>`root@vmi653640:~# rly q balance umee-betanet-1` <br/>
>`31332transfer/channel-0/utki,73115uumee` <br/>
>`root@vmi653640:~# rly q balance kichain-t-4` <br/>
>`11332transfer/channel-61/uumee,10058468utki` <br/>
  
>Hash details for a transaction through the Umiya network can be viewed on the following path in the explorer
>```
>https://api-challenge.blockchain.ki/txs/<hash>
>```

### Performance cross-network transaction from KiChain to Umee on KiChain node server
>⚠️ This step are performed on Kichain server <br/>
Template for transaction from KiChain to Umee network
```bash
kid tx ibc-transfer transfer transfer <src-port> <src-channel> <receiver> <amount> <flags>
```
The required channel can be found in the command execution results on the server where the relay is installed (an example is present in the text above) 
```bash
rly paths show transfer
```
>An example for our wallet:<br/>
>`kid tx ibc-transfer transfer transfer channel-61 umee1ymx74ypkktunu59ks00jaw5cd66nwv0khzlgnr 10000utki --from $kichain_wallet_name --fees=1000utki --gas=auto --chain-id kichain-t-4 --home /root/testnet/kid/ -y`

>Hash details for a transaction through the Umiya network can be viewed on the following path in the explorer
>```
>https://api-challenge.blockchain.ki/txs/<hash>
>```

### Hashs of the performed Transactions
  
>Details on the newly created wallets can be viewed on the following path in the explorers<br/>
>(In Umee explorer to view coins of different networks, we need a drop-down flag "Select coin". For the Kitchenain network, there will be an empty value.)
>```
>https://explorer-umee.nodes.guru/account/<UMEE_WALLET_NAME_ADDRESS><br/>
>https://ki.thecodes.dev/address/<KICHAIN_WALLET_NAME_ADDRESS>
>```
Details of our wallets from the example <br/>
https://explorer-umee.nodes.guru/account/umee1ymx74ypkktunu59ks00jaw5cd66nwv0khzlgnr <br/>
https://ki.thecodes.dev/address/tki1e7vtgqh63u8vll45jan98lxx72pfgs59wm9azx
 
Hashs of performance cross-network transaction from Umee to KiChain on Umee node server
[B59D8C0908ED548C10A819B3F66120CDFF02A0A810964B54A1089F2B5626394A](https://explorer-umee.nodes.guru/transactions/B59D8C0908ED548C10A819B3F66120CDFF02A0A810964B54A1089F2B5626394A) <br/>
[9C9E28F46ADBD4EA42DA9C8D7C56CA7118ACD20B9D33574AAE26C68ADB720752](https://explorer-umee.nodes.guru/transactions/9C9E28F46ADBD4EA42DA9C8D7C56CA7118ACD20B9D33574AAE26C68ADB720752) <br/>
[B1D16C3C6C3048262C398EAA13B0C345ACD4DD50A7A2B176B7136E64D5B9CC45](https://explorer-umee.nodes.guru/transactions/B1D16C3C6C3048262C398EAA13B0C345ACD4DD50A7A2B176B7136E64D5B9CC45) <br/>
[44848AC48F56B97AEBF97A3AF551AD706B434C2CFDA7883D1B1074599BEBDBF1](https://explorer-umee.nodes.guru/transactions/44848AC48F56B97AEBF97A3AF551AD706B434C2CFDA7883D1B1074599BEBDBF1) <br/>
[82A87FC92FCD5F099D4E42522DD234ADC5A4933DB3DABE15804430E3ECDF79B4](https://explorer-umee.nodes.guru/transactions/82A87FC92FCD5F099D4E42522DD234ADC5A4933DB3DABE15804430E3ECDF79B4) <br/>
[B6D1A056094A4C000AC0CC3106F96B61588D74B92035EE099402E97925577C5C](https://explorer-umee.nodes.guru/transactions/B6D1A056094A4C000AC0CC3106F96B61588D74B92035EE099402E97925577C5C)   

Hashs of performance cross-network transaction from KiChain to Umee on Umee node server
[35DF94E698F59C1D8A50BB6BC4433C39DFAFAED42B394AB3879460FA95B0CC6F](https://api-challenge.blockchain.ki/txs/35DF94E698F59C1D8A50BB6BC4433C39DFAFAED42B394AB3879460FA95B0CC6F) <br/>
[A8067CD460FA4B866D98B55A426736C683F4721622F21CD02E74B7934DDD42D6](https://api-challenge.blockchain.ki/txs/A8067CD460FA4B866D98B55A426736C683F4721622F21CD02E74B7934DDD42D6) <br/>
[E7E74B5FC665F0C7C973E68048CDC4EC205274589406810422ADD24BE2E2FF6B](https://api-challenge.blockchain.ki/txs/E7E74B5FC665F0C7C973E68048CDC4EC205274589406810422ADD24BE2E2FF6B) <br/>
[E2FA114AD7DC44152E1A3095B6C3D838AF6009DCCC2CDD467182963182DA1F3A](https://api-challenge.blockchain.ki/txs/E2FA114AD7DC44152E1A3095B6C3D838AF6009DCCC2CDD467182963182DA1F3A) <br/>
[DA6E1454CE738D7F7FEA15E4E6288DD2840B9D91F846308E1B44CD1154AFF293](https://api-challenge.blockchain.ki/txs/DA6E1454CE738D7F7FEA15E4E6288DD2840B9D91F846308E1B44CD1154AFF293)
  
Hashs of performance cross-network transaction from KiChain to Umee on KiChain node server
[67895FD8EEF20E15F2E1675635C42480FCEA8DA7535CCC97810B9FED5852FDC1](https://api-challenge.blockchain.ki/txs/67895FD8EEF20E15F2E1675635C42480FCEA8DA7535CCC97810B9FED5852FDC1) <br/>
[2C9AC9F2C32A492D973E78B52484BDB353CCFC7B616B6FB2970CC9E8394E110D](https://api-challenge.blockchain.ki/txs/2C9AC9F2C32A492D973E78B52484BDB353CCFC7B616B6FB2970CC9E8394E110D) <br/>
[CEFE1D4AD4ED074D68D62F0C936B3636F2F7620A1EF2D6112AA0C34DBBF1D901](https://api-challenge.blockchain.ki/txs/CEFE1D4AD4ED074D68D62F0C936B3636F2F7620A1EF2D6112AA0C34DBBF1D901) <br/>
[335287ECB2281E089BC2A952849508E5C69F67569F34D62C6D1D1092056F1918](https://api-challenge.blockchain.ki/txs/335287ECB2281E089BC2A952849508E5C69F67569F34D62C6D1D1092056F1918)
<br/>
<br/>
<br/>
We have performed IBC transaction between Umme and Kichain blockchains 📲.

## Installation Requirements
1. Install Golang. You can follow the steps on their official website https://golang.org/doc/install/.
2. Install Relayer. I'm using cosmos relayer on https://github.com/cosmos/relayer/.
```
git clone git@github.com:cosmos/relayer.git
git checkout v0.9.3
cd relayer && make install
```
Or you can use binary file already available at https://github.com/cosmos/relayer/releases/. Then extract the compressed file with tar
`tar -xzvf <FILE_NAME>`
# Using Relayer
3. Initialize relayer `rly config init` or you you can also set the home path by adding the flag `--home <PATH>` to the command
4. Create a config file with .json format for your chain id as below (each chain has different file contents).
```
{
  "chain-id": "<CHAIN_ID>",
  "rpc-addr": "http://<NODE_IP>:<NODE_RPC_PORT>",
  "account-prefix": "<CHAIN_PREFIX>",
  "gas-adjustment": 1.5,
  "gas-prices": "0.025<CHAIN_DENOM>",
  "trusting-period": "48h"
}
```
Example
```
{
  "chain-id": "kichain-t-4",
  "rpc-addr": "http://localhost:26657",
  "account-prefix": "tki",
  "gas-adjustment": 1.5,
  "gas-prices": "0.025utki",
  "trusting-period": "48h"
}
```
5. Do step number 4 for 2 different chain id
6. Add chain config to relayer `rly chains add -f <FILE_CONFIG_NAME>`.
<br> Example `rly chains add -f rlyki.json`
7. Add key for each chain id.
`rly keys add <CHAIN_ID> <KEYS_NAME>`
<br> Example `rly keys add kichain-t-4 cygnus`
<br> Or you can recover existing key with mnemonic.
`rly keys restore <CHAIN_ID> <KEY_NAME> "<MNEMONIC>"`
8. Enter the key name on the relayer according to the chain id `rly chains edit <CHAIN_ID> key <KEY_NAME>`
<br> Example `rly chains edit kichain-t-4 key cygnus`
9. Add the balance on the key for the transaction
10. Initialize light sync for each chain id `rly light init <CHAIN_ID> -f`
<br> Example `rly light init kichain-t-4 -f`
11. Generate path for a pair of chain id `rly paths generate <CHAIN_ID_1> <CHAIN_ID_2> <PATH_NAME>`
<br> Example `rly paths generate kichain-t-4 lucina ibcchallenge`
12. Create channels and connections for cross chain transactions `rly tx link <PATH_NAME>`
<br> Example `rly tx link ibcchallenge`
13. Start relayer `rly start`
14. Try to transfer some coin to another chain id `rly transact transfer <FROM_CHAIN_ID> <TO_CHAIN_ID> <AMOUNT> <TO_ADDRESS>`
<br> Example `rly tx transfer lucina kichain-t-4 1000000ujuno tki1qltym5huvg9j04vw3dn98ywwfe45s6tc6sr0at`
<br> You will see the transaction hash to check on the explorer `https://ki.thecodes.dev/tx/<TX_HASH>`

Example for the some transactions
```
https://ki.thecodes.dev/tx/DF56308EAC9750355C7AA3CD44987A250F6A21ECA91E3E549E899A3B7DC54EE4
https://ki.thecodes.dev/tx/AD5E469535A7599B0CA411985A4F6D1F6715DE1D16315E1B7A72A80ABA34A518
https://ki.thecodes.dev/tx/F09E0B7B5647AFBAF98C3B33FA54FD178704069F79980418DB36DB9137A8B5BD
https://ki.thecodes.dev/tx/FD0636E69821C16B0B868CA51D4604754D8DBA57A74106E18DE3DFF65A29AAD9
https://ki.thecodes.dev/tx/A5D1A2F26C10956998DC5B1EDA93479410B51B9AE9CDF6D065D93B3B3197FDD6
https://ki.thecodes.dev/tx/78CA4A165AB0A1E503D441B77918138E90BCFC4CA0C137E673D054DF669AD335
```

## Commands that will help
- Show chain id list `rly chains list`
- Show paths list `rly paths list`
- Show account balance by chain id key `rly q balance <CHAIN_ID>`

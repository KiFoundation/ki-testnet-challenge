Relayer Info

I am using go-relayer, if you want you can use typescript or rust relayer.

Installation

git clone https://github.com/cosmos/relayer.git
cd relayer
git checkout v0.9.3
make install

Setup

Initiate the relayer

rly config init


Note: Above command will create relayer folder in home directory with default config.yaml file

Go to cd ~/.relayer/config & add both chains configuration.

Chain – 1
Create json file with chain 1 configurations.

 	nano  kichain-t-4.json
{
  "chain-id": "kichain-t-4",
  "rpc-addr": "http://xxx.x.x.x:26657",
  "account-prefix": "tki",
  "gas-adjustment": 1.5,
  "gas-prices": "0.025utki",
  "trusting-period": "48h",
  "key": "wallet_name"
}
rly chains add -f  kichain-t-4.json

Chain -2 
Create json file with chain21 configurations.

 	nano  autonomy.json
{
  "chain-id": "autonomy",
  "rpc-addr": "http://20.42.119.7:26657",
  "account-prefix": "autonomy",
  "gas-adjustment": 1.5,
  "gas-prices": "1aut",
  "trusting-period": "336h",
  "key": "testkey"
}
rly chains add -f  autonomy.json


Check chains status
rly chains list


Adding keys
Note: you can use same mnemonic phrase used in Ki chain, for both Ki chain and autonomy chain.

Adding ki test net keys to relayer
rly keys restore kichain-t-4  testkey "mnemonic phrase"

Adding autonomy keys to relayer
you can use ki seed to recover autonomy key through relayer.
rly keys restore autonomy  testkey "mnemonic phrase"

Query balance
To verify configuration properly you can use account query in both chains
rly q bal kichain-t-4  testkey

You can get the test tokens for autonomy

curl --header "Content-Type: application/json"   --request POST   --data '{"denom":"aut","address":"autonomy1jlqavmq6lrz2s7rrpjh0epepdzgak384zzf5xj"}'   http://20.42.119.7:8000/credit

rly q bal autonomy  testkey

Init lightclients

rly light init kichain-t-4 -f
rly light init autonomy -f

Now check the chain status

rly chains list     
Path generation

rly paths gen kichain-t-4 autonomy <path>
Link the both chains

rly tx link <path> -d

Note: This will create client, connection, channels between two chains.

Start Relayer

rly start <path>
IBC Transactions:

from kichain to autonomy

rly tx  xfer kichain-t-4 autonomy 1utki <reciver-autonomy-address> --path kitoatn -d

from autonomy to kichains

rly tx xfer autonomy kichain-t-4  1aut tki1ghzd9t0zj23ssew7zv8sg97l9xakh8r8nxmr4l  --path kitoatn -d
 


Transaction hash will be generated.

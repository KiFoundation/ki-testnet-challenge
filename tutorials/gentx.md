The first step of the KiChain testnet challenge is to initiate a new testnet from scratch. Therefore, participants are required to create the keys of their validators and to generate their genesis transactions.  

Following are the System requirements to run a node on the KiChain testnet:
- Ubuntu 18.04 OS or later
- 4 Cores
- 4GB RAM
- 80GB SSD at least

Following is the process of creating the validator keys and the genesis transaction:

Download and install Go v1.13.5+ )

```bash
wget https://dl.google.com/go/go1.13.5.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.13.5.linux-amd64.tar.gz
```

Export Go paths

```bash
GOPATH=/usr/local/go
PATH=$GOPATH/bin:$PATH
mkdir -p $HOME/go/bin
echo "export PATH=$PATH:$(go env GOPATH)/bin" >> ~/.bash_profile
source ~/.bash_profile
```

Test the installation

```bash
go version
```

Clone and install `ki-tools`

```bash
git clone https://github.com/KiFoundation/ki-tools.git
cd ki-tools
git checkout testnet
make install
```

Check the installed version

```json
kid version --long
```

This should ouput
```bash
name: ki-tools
server_name: kid
client_name: kicli
version: 0.1-13-g711e19e-Testnet
commit: 711e19ebbb516ae6d38c638634c4bef05201be72
build_tags: netgo,ledger
go: go version go1.16 linux/amd64
```

Create node directories:  

```bash
export NODE_ROOT= <location of your choice>
mkdir -p $NODE_ROOT/kid $NODE_ROOT/kicli $NODE_ROOT/kilogs
cd $NODE_ROOT
```

Initiate the node files

```bash
kid init <your-validator-moniker> --chain-id kichain-t-2 --home ./kid/
```

Create the validator account. Do not forget to save the mnemonic.

```bash
kicli keys add <wallet-name> --home ./kicli/
```

Feed the validator wallet with 100tki

```bash
kid add-genesis-account $(kicli keys show <wallet-name> -a --home kicli/ ) 100000000utki --home kid/
```

Generate the genesis transaction for the validator creation

```bash
kid gentx \
	--commission-max-change-rate=0.1 \
	--commission-max-rate=0.1 \
	--commission-rate=0.1 \
	--min-self-delegation=1 \
	--amount=100000000utki \
	--pubkey `kid tendermint show-validator --home ./kid/` \
	--name=<wallet-name> \
	--home ./kid/ \
	--home-client ./kicli/
```

this generates a file called `gentx-<node-id>.json` in `$NODE_ROOT/kid/config/gentx/`. Run the following commands to fetch the validator addresses needed to fill the [registration form](https://forms.gle/AxNdZQ7qeGiQfmjy7).

(The following step requires `jq`. It can be installed with `sudo apt-get install jq`. You can skip installing `jq` and manually fetch the information below in the file).  

Validator testnet wallet address:
```bash
cat $NODE_ROOT/kid/config/gentx/gentx-<node-id>.json | jq .value.msg[0].value.delegator_address
```

Validator testnet operator address:
```bash
cat $NODE_ROOT/kid/config/gentx/gentx-<node-id>.json | jq .value.msg[0].value.validator_address
```


Note: Another information found in the gentx file is the node address `"memo":"node_id@ip:port"`. This is the address used by other peers to connect to your node. Depending on your server setup, the IP added in the file by the gentx command can be a private one (thus unusable). If this is the case, please change it manually to the public IP of your node (change only the IP). 

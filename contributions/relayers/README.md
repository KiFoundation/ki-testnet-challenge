<p align="right">
    <img width=150px src="https://wallet-testnet.blockchain.ki/static/img/icons/ki-chain.png" />
</p>


This directory hosts the contributions for the IBC relayer Task.

## Task instructions:

To accomplish the this task, the following steps need to be performed:
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

Contributions should be submitted to the ki-testnet-challenge repo under the following directory:
https://github.com/KiFoundation/ki-testnet-challenge/tree/main/contributions/relayers

The PR submission deadline is:  `Monday 6th of September at 23:59UTC`.

Please note that any PR made after the deadline or in the wrong directory will be automatically rejected.


File `<github_username>-<moniker>.json` (do not forget to replace `<github_username>` with you github username and  `<moniker>` with your validator moniker):
```
{
   "moniker": "Your validator moniker goes here",
   "documentationURL": "The link to your Readme or Medium post",
   "ibcTransferTxHashs": ["a list of your first 5 ibc transaction"],
   "additionalComments": "Any adittional comments you would like to add about your contribution"
}
```
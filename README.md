<p align="right">
    <img width=150px src="https://wallet-testnet.blockchain.ki/static/img/icons/ki-chain.png" />
</p>

# Ki Testnet Challenge
This repository hosts `ki-testnet-challenge`. A set of scripts and resources to be used for the Ki Testnet Challenge

## What is it
The Testnet Challenge consists of a series of more or less technical tasks related to the validator operator role on the KiChain. You will be invited to explore the smallest details of the KiChain. During the course of the challenge, the tasks get progressively more difficult, they range from “do it whenever/however you want” tasks to “be ready to spend few hours on this one” tasks.

To know more about the challenge read the dedicated post [here](https://medium.com/ki-foundation/announcing-the-kichain-challenge-incentivized-testnet-420006b48535)

## Prizes
A total of **100 000 USD** in XKIs is allocated for rewards, split as follow :
- 50 000 USD for the winner
- 20 000 USD for the 2nd
- 5 000 USD for the 3rd
- 3 000 USD for the 4th to the 10th
- 4 000 USD bonus prizes for special challenges

Please note that the prizes are subject to a 12 months linear monthly vesting.

Aside from these prizes, **1 000 000 USD** of XKIs will be distributed as delegations to the mainnet validators belonging to winners from rank 11 to 20 included. Please note that only validators offering commission fees under 10% are eligible for this prize.

## How to Participate
&#9888;  **REGISTRATIONS ARE OPEN**   &#9888;

To participate to the testnet challenge, please follow these steps:
1. Join the Ki Ecosystem Discord [here](https://discord.gg/D3vvEeBpE5)  
2. Generate your validator keys by following [this tutorial](tutorials/gentx.md).
3. Fill the registration [form]().
4. Add your validator to the genesis:
  - rename your gentx generated in step 2 and found in `<NODE_ROOT>/kid/config/gentx/gentx-<node-id>.json` to `gentx-<moniker>.json`
  - add it to the gentx directory in the [network repo](https://raw.githubusercontent.com/KiFoundation/ki-networks/v0.1/Testnet/kichain-t-2/gentx) by opening a Pull Request.

## Leader board

| rank | Moniker | Points |
| ---- | ------- | ------ |
|      |         |        |

## Disclaimer
The Ki Foundation reserves the right in its sole discretion to amend or change or cancel this challenge at any time and for any reasons without prior notice.

## Security
If you discover a security vulnerability in this project, please report it to security@foundation.ki. We will promptly address all security vulnerabilities.

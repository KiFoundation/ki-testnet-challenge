# Read gentx
# Extract accounts
# Build supply accounts
# Add accounts to genesis
# Add gentx to genesis
# write genesis

import json
from os import listdir
from os.path import isfile, join

gentx_dir = './gentx/'
accounts_dir = './accounts/'
genesis_raw_file = 'genesis_raw.json'
amount_per_genesis_account = 1000000000  # uxki
leftovers_wallet_address = 'tki1v4gtuws5y55maldz5wpxyjpp4yxduq2w9hp93z'

# get gentex and account file names
gentx_files = [f for f in listdir(gentx_dir) if isfile(join(gentx_dir, f)) and f[-4:] == 'json']
account_files = [f for f in listdir(accounts_dir) if isfile(join(accounts_dir, f)) and f[-4:] == 'json']

accounts_dict = dict()
gentx_genesis_obj = []
accounts_genesis_obj = []
total_balances = 0
total_supply = 100000000000000

def buidl_account_object(address, amount):
    account_template = json.loads(
        '{"address": "", \
        "coins": [{"denom": "utki","amount": ""}], \
        "sequence_number": "0", \
        "account_number": "0", \
        "original_vesting": [], \
        "delegated_free": [], \
        "delegated_vesting": [], \
        "start_time": "0", \
        "end_time": "0", \
        "module_name": "", \
        "module_permissions": [""]}'
    )

    account_template['address'] = address
    account_template['coins'][0]['amount'] = amount

    return json.dumps(account_template)

# Read all gentx files
for gentx_file in gentx_files[:2]:
    print('Reading ', gentx_file, ' ', end="")
    f = open(join(gentx_dir, gentx_file))
    try:
        # get the gentx object and append it to the genesis gentx array
        gentx = json.load(f)
        gentx_genesis_obj.append(gentx)
        print()
        # insert the account into the account dict with the preset amount
        accounts_dict[gentx['value']['msg'][0]['value']['delegator_address']] = str(amount_per_genesis_account)
        total_balances += amount_per_genesis_account
    except:
        print(' failed')

# Read all account files
for account_file in account_files:
    print('Reading ', account_file, ' ', end="")
    f = open(join(accounts_dir, account_file))
    try:
        # get the account object and append it to the genesis account array
        account = json.load(f)
        accounts_dict[account['account']] = account['amount']
        print()
    except:
        print(' failed')

# Feed the "leftovers" account with the remainder supply tokens
remaining_supply = total_supply - total_balances
accounts_dict[leftovers_wallet_address] = str(remaining_supply)

# Append the validator accounts to the genesis account array from the dict
for key, val in accounts_dict.items():
    accounts_genesis_obj.append(
        json.loads(buidl_account_object(key, val))
    )

# Read genesis object
f = open(join(genesis_raw_file))
genesis = json.load(f)
genesis['app_state']['accounts'] = accounts_genesis_obj
genesis['app_state']['genutil']['gentxs'] = gentx_genesis_obj

print(json.dumps(genesis))

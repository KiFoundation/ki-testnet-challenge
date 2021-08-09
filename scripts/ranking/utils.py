import json
import pickle
import binascii
import requests
import numpy as np
import configparser

from pathlib import Path
from bip_utils import AtomBech32Decoder, AtomBech32Encoder

config = configparser.ConfigParser()
config.read("./config.ini")
network = config["COMMON"]["Network"]
api = config[network]["Api"]
netprefix = config[network]["Prefix"]
validators_dir = config["COMMON"]["Validators"]
signing_info_dir = config["COMMON"]["SigninfInfo"]
signing_info_state = config["COMMON"]["CurlState"]


def dump_data(data, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump(data, f)


def load_data(file_name):
    with open(file_name, 'rb') as f:
        data = pickle.load(f)

    return data


def get_current_height():
    r = requests.get(api + "/blocks/latest")
    return r.json()["block"]["header"]["height"]


def get_validators_conspub_to_valoper():
    validators = {}
    unbonding_heights = []
    r = requests.get(api + "/staking/validators?status=unbonded")
    temp = r.json()["result"]
    for val in temp:
        validators[val["consensus_pubkey"]] = val["operator_address"]
        unbonding_heights.append(val["unbonding_height"])

    r = requests.get(api + "/staking/validators?status=unbonding")
    temp = r.json()["result"]
    for val in temp:
        validators[val["consensus_pubkey"]] = val["operator_address"]
        unbonding_heights.append(val["unbonding_height"])

    r = requests.get(api + "/staking/validators?status=bonded")
    temp = r.json()["result"]
    for val in temp:
        validators[val["consensus_pubkey"]] = val["operator_address"]
        unbonding_heights.append(val["unbonding_height"])

    unbonding_heights = list(np.unique(unbonding_heights))
    unbonding_heights.append(get_current_height())

    dump_data(validators, validators_dir + "validators_conspub_to_valoper.pickle")
    return validators, unbonding_heights


def get_validators_conspub_to_cons(unbonding_heights):
    validators = {}

    for height in unbonding_heights[1:]:
        r = requests.get(api + "/validatorsets/" + height)
        validators_ = r.json()["result"]["validators"]

        for val in validators_:
            validators[val["pub_key"]] = val["address"]

    dump_data(validators, validators_dir + "validators_conspub_to_cons.pickle")

    return validators


def get_validators_address_to_valoper(validators_conspub_to_cons, validators_conspub_to_valoper):
    validators = {}
    for key, val in validators_conspub_to_cons.items():
        validators[str.upper(bech32_to_addresses(val, netprefix + "valcons"))] = validators_conspub_to_valoper[key]

    dump_data(validators, validators_dir + "validators_address_to_valoper.pickle")

    return validators


def addresses_to_bech32(address, prefix):
    bytes = binascii.unhexlify(str.encode(address))
    enc = AtomBech32Encoder.Encode(prefix, bytes)
    return enc


def bech32_to_addresses(bech32, prefix):
    dec = AtomBech32Decoder.Decode(prefix, bech32)
    return dec.hex()


def get_all_signing_infos():
    signing_info_files = [str(file) for file in Path(signing_info_dir).glob('signing_info_*.csv')]
    return signing_info_files


def get_latest_state():
    state = {
        "start": -1,
        "end": -1
    }
    try:
        with open(signing_info_state) as json_file:
            state = json.load(json_file)
    except FileNotFoundError:
        pass

    return state


def write_latest_state(start, end):
    state = {
        "start": start,
        "end": end
    }
    with open(signing_info_state, 'w') as json_file:
        json.dump(state, json_file)
    return


def update_all():
    cpto, uh = get_validators_conspub_to_valoper()
    cptc = get_validators_conspub_to_cons(uh)
    ato = get_validators_address_to_valoper(cptc, cpto)
    return cpto, cptc, ato


get_all_signing_infos()

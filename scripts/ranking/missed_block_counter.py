import time
import utils
import random
import requests
import configparser
import pandas as pd
import multiprocessing as mp

config = configparser.ConfigParser()
config.read("./config.ini")
network = config["COMMON"]["Network"]
api = config[network]["Api"]
validators_dir = config["COMMON"]["Validators"]
signing_info_dir = config["COMMON"]["SigninfInfo"]
signing_info_raw_dir = config["COMMON"]["SigninfInfoRaw"]
random_delays = bool(int(config["COMMON"]["RandomDelays"]))
update_validator_list = bool(int(config["COMMON"]["UpdateValidatorList"]))
curl_mode = config["COMMON"]["CurlMode"]
curl_window = config["COMMON"]["CurlWindow"]
curl_direction = config["COMMON"]["CurlDirection"]
end_height = config["COMMON"]["CurlEndHeight"]
start_height = config["COMMON"]["CurlStartHeight"]

n_blocks = 1
if curl_window == 'minutes':
    curl_interval_min = int(config["COMMON"]["CurlIntervalMin"])
    n_blocks = int(curl_interval_min * 60 / 5)

if curl_window == 'blocks':
    n_blocks = int(config["COMMON"]["BlocksToCurl"])


def get_signers_at_height(h):
    block = {}
    r = requests.get(api + "/blocks/" + str(h))
    block["height"] = r.json()["block"]["header"]["height"]
    precommits = r.json()["block"]["last_commit"]["precommits"]
    block["signers"] = []

    for pc in precommits:
        try:
            block["signers"].append(pc["validator_address"])
        except:
            pass

    if random_delays:
        delay = random.betavariate(1, 20)
        time.sleep(delay)

    return block


def get_n_latest_blocks_p(heights_):
    pool = mp.Pool(mp.cpu_count())
    results = pool.map(get_signers_at_height, heights_)
    return results


def build_signing_matrix(heights_, validators_, signers_):
    validators_atv = utils.load_data("data/validators/validators_address_to_valoper.pickle")
    validator_matrix = pd.DataFrame(0, index=validators_, columns=heights_)
    for item in signers_:
        for signer in item["signers"]:
            validator_matrix.loc[validators_atv[signer]][int(item["height"])] = 1

    return validator_matrix


def count_missed_blocks():
    start_execution_time = time.time()

    # Fetch validator list
    if update_validator_list:
        # Update the valdiator list
        validators = utils.update_all()[0].values()
    else:
        # Fetch from dumped state
        validators = utils.load_data(validators_dir + "validators_conspub_to_valoper.pickle").values()

    # Compute the first and last heights
    if curl_direction == "backward":
        end_height_ = int(end_height) if end_height != "current" else int(utils.get_current_height())
        start_height_ = end_height_ - n_blocks
    else:
        state = int(utils.get_latest_state()["end"]) if int(utils.get_latest_state()["end"]) > 0 else int(start_height)
        start_height_ = int(start_height) if curl_mode == "spot" else state
        end_height_ = start_height_ + n_blocks

    # Build the height array and fetch the blocks in a parallel manner
    heights = [h for h in range(end_height_, start_height_, -1)]
    signers = get_n_latest_blocks_p(heights)

    # Build and dump the signature matrix
    signed = build_signing_matrix(heights, validators, signers)
    utils.dump_data(signed, signing_info_raw_dir + "raw_signing_info_%s_%s_%s.pickle" % (start_height_, end_height_, int(start_execution_time)))

    # Compute signed and missed blocks and store them in csv
    signed['total_signed'] = signed.sum(axis=1)
    signed['total_missed'] = (end_height_ - start_height_) - signed["total_signed"]
    signed[['total_signed', 'total_missed']].to_csv(signing_info_dir + "signing_info_%s_%s_%s.csv" % (start_height_, end_height_, int(start_execution_time)), index_label="validator")

    utils.write_latest_state(start_height_, end_height_)
    print("Execution time %s ms" % ((time.time() - start_execution_time) * 1000))


def merge_missed_blocks_data(start, end):
    files = utils.get_all_signing_infos()
    all_signing_infos = pd.read_csv(files[0])
    for file in files[1:]:
        temp_matrix = pd.read_csv(file)
        all_signing_infos["total_signed"] = all_signing_infos["total_signed"] + temp_matrix["total_signed"]
        all_signing_infos["total_missed"] = all_signing_infos["total_missed"] + temp_matrix["total_missed"]

    return all_signing_infos


if __name__ == '__main__':
    count_missed_blocks()
    # merge_missed_blocks_data(0, 0)

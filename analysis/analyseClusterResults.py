import csv

import pandas as pd


def analyseModalShare(trips, personsInVelbert, runId):
    modes_full = ["bike", "car", "pt", "ride", "walk"]
    modes_comp = ["bike", "car", "pt", "walk"]

    desired_modal_share = {
        "bike": 0.098,
        "car": 0.563,
        "pt": 0.084,
        "walk": 0.254
    }

    # filter persons
    personMask = trips["person"].isin(personsInVelbert)
    tripsMask = trips["longest_distance_mode"].notnull()
    trips = trips[personMask & tripsMask]
    number_of_trips = trips.shape[0]

    # calculate modal share
    stat = trips.groupby(["longest_distance_mode"]).count()["trip_id"] / number_of_trips

    modal_share = dict([(m, stat[m]) for m in modes_full])
    modal_share["car"] = modal_share["car"] + modal_share["ride"]
    modal_share.pop("ride")

    assert abs(
        sum(modal_share.values()) - 1.0) < 0.01, f"Modal share does not sum up to 100%, but to {sum(modal_share.values())}"

    # write modal share
    with open("resultShares.csv", "a", newline="") as resultCsv:
        writer = csv.writer(resultCsv, delimiter=";")
        writer.writerow(
            [runId, desired_modal_share["pt"] - modal_share["pt"], desired_modal_share["bike"] - modal_share["bike"],
             desired_modal_share["car"] - modal_share["car"], desired_modal_share["walk"] - modal_share["walk"]])


ids = range(115, 127)

baseString = "velbert-v1.0-1pct.output_trips{0}.csv"

path_to_txt = "../src/main/resources/personIdsFromVelbert.txt"

with open(path_to_txt) as f:
    personsInVelbert = f.readlines()
personsInVelbert = [int(p.strip("\n")) for p in personsInVelbert]

for i in ids:
    trips = pd.read_csv("trips/" + baseString.format(i), delimiter=";")
    analyseModalShare(trips, personsInVelbert, i)

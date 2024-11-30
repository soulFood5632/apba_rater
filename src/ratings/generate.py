import warnings

import numpy as np

import src.ratings.predictor as predictor
import src.utils.database as db


def generate_faceoff():
    hr_data = db.load_hr(["14-15", "15-16", "16-17", "17-18", "18-19", "19-20", "20-21", "21-22", "22-23"])
    print(f"Collected {len(hr_data)} entries")
    relevant_table = hr_data[["Player", "season", "Pos", "GP", "FOW", "FOL"]]

    ratings = []
    for gp, w, l in zip(relevant_table["GP"], relevant_table["FOW"], relevant_table["FOL"]):
        pred_rating = predictor.ci_face_off_rating(gp, w, l) * 5
        try:
            ratings.append(int(pred_rating))
        except:
            warnings.warn(f"Could not convert {pred_rating} to an integer")
            ratings.append(0)
    print(f"Generated {len(ratings)} ratings")

    relevant_table["FaceoffRating"] = ratings
    file_path = "data/generated/FaceoffRating.csv"

    print(f"Saving the data to {file_path}")
    relevant_table.to_csv(file_path, index=False)
    print("SUCCESS!")


def generate_defence():
    hr_data = db.load_hr(["14-15", "15-16", "16-17", "17-18", "18-19", "19-20", "20-21", "22-23"])
    print(f"Collected {len(hr_data)} entries")

    relevant_table = hr_data[
        [
            "Player",
            "season",
            "Pos",
            "GP",
            "ATOI",
            "BLK",
            "CorsiForPerc",
            "FenwickPerc",
            "CorsiForPercRel",
            'FenwickPercRel',
            'CorsiAgainst',
            'DZoneStartPerc',
            'GAPer60',
            'XGA',
            'XGF',
            'GFPer60'
        ]
    ]

    relevant_table["ATOI"] = relevant_table.apply(lambda x: convert_time(x["ATOI"]), axis=1)
    relevant_table['exGA60'] = relevant_table['XGA'] / relevant_table['GP'] / relevant_table['ATOI'] * 3600
    relevant_table['exGF60'] = relevant_table['XGF'] / relevant_table['GP'] / relevant_table['ATOI'] * 3600
    relevant_table['BLK_60'] = relevant_table['BLK'] / relevant_table['GP'] / relevant_table['ATOI'] * 3600
    relevant_table['CorsiAgainst_60'] = relevant_table['CorsiAgainst'] / relevant_table['GP'] / relevant_table[
        'ATOI'] * 3600

    ratings = {}
    available_seasons = set(relevant_table["season"])
    print(f"Found {available_seasons}")

    for season in available_seasons:
        ratings[season] = []

        season_filtered = relevant_table[relevant_table["season"] == season]
        print(f"Found {len(season_filtered)} entries for {season}")

        for atoi, ga60, gf60, exga60, exgf60, corsi_a_60, d_zone_start, position, corsi_relative in zip(
                season_filtered["ATOI"],
                season_filtered["GAPer60"],
                season_filtered["GFPer60"],
                season_filtered["exGA60"],
                season_filtered["exGF60"],
                season_filtered["CorsiAgainst_60"],
                season_filtered["DZoneStartPerc"],
                season_filtered["Pos"],
                season_filtered["CorsiForPercRel"]
        ):

            pred_rating = predictor.ci_defense_rating(
                atoi, ga60, gf60, exga60, exgf60, corsi_a_60, d_zone_start, position, corsi_relative
            )
            if np.isnan(pred_rating):
                warnings.warn(f"Could not convert {pred_rating} to an integer")
                pred_rating = 0
            ratings[season].append(pred_rating)

        # TODO: Double check these distribution values
        rating_distribution = {1: 0.1, 2: 0.31, 3: 0.34, 4: 0.2, 5: 0.05}
        adjusted_ratings = predictor.bucketing_and_map(rating_distribution, ratings[season])
        ratings[season] = adjusted_ratings

        season_filtered["DefenceRating"] = adjusted_ratings
        print(f"Generated {len(adjusted_ratings)} ratings for {season}")
        # we will join on the index values
        relevant_table.loc[relevant_table["season"] == season, "DefenceRating"] = adjusted_ratings

    file_path = "data/generated/DefenceRating.csv"

    print(f"Saving the data to {file_path}")
    relevant_table.to_csv(file_path, index=False)
    print("SUCCESS!")


def convert_time(atoi: str):
    """
    Converts the time in the format of MM:SS to seconds.

    MM:SS is the default format used by hockey reference
    :param atoi: the time in the format of MM:SS
    :return: the number of seconds that the time represents
    """
    times = atoi.split(":")
    return int(times[0]) * 60 + int(times[1])


if __name__ == "__main__":
    generate_defence()

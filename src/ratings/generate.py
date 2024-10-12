from typing import Literal
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
            ratings.append(0)
    print(f"Generated {len(ratings)} ratings")

    relevant_table["FaceoffRating"] = ratings
    file_path = "data/generated/FaceoffRating.csv"

    print(f"Saving the data to {file_path}")
    relevant_table.to_csv(file_path, index=False)
    print("SUCCESS!")


def generate_defence():
    pass

from typing import List

import pandas as pd
import streamlit as st
import os

from src.utils.database import load_hr, load_all_apba

st.set_page_config(layout="wide")

available_stats = ["Faceoff", "Defence", "Passing"]
ground_truth_data = load_all_apba()
generated_data = {
    "Faceoff": pd.read_csv("data/generated/FaceoffRating.csv"),
}

name_options = {f"{player_name}" for player_name in ground_truth_data["Player"]}

year_options = {f"{year}" for year in ground_truth_data["season"]}


def filtered_rating_data(
    rating: str, selected_players: List[str], selected_years: List[str], ignore_failed_matches:
    bool
):
    # this below code prepares the apba data for the selected players and years.
    print(ground_truth_data.columns)

    if rating == "Defence":
        defense_rating = [
            max(x) for x in zip(
                ground_truth_data["RateCDefence"].tolist(),
                ground_truth_data["RateRWDefence"].tolist(),
                ground_truth_data["RateLDDefence"].tolist(),
                ground_truth_data["RateRDDefence"].tolist(),
                ground_truth_data["RateLWDefence"].tolist()
            )
        ]
        rating_filtered = ground_truth_data[
            ["Player", "season"]
        ]

        rating_filtered[f"Rate{rating}"] = defense_rating
    else:
        rating_filtered = ground_truth_data[["Player", "season", f"Rate{rating}"]]

    generated_data_rating = generated_data[rating]

    merged = pd.merge(
        rating_filtered, generated_data_rating, on=["Player", "season"],
        how="inner" if ignore_failed_matches else "outer"
    )

    name_filtered = merged[
        merged["Player"].isin(selected_players)
    ]

    year_filtered = name_filtered[name_filtered["season"].isin(selected_years)]

    return year_filtered


def main():
    st.title("APBA Rating Demo")

    rating = st.selectbox("Choose a rating...", options=available_stats)

    st.header("Filters")
    selected_players = st.multiselect("Choose a player name...", options=name_options, default=["Connor McDavid"])
    selected_years = st.multiselect(
        "Choose years...", options=year_options, default=sorted({x for x in year_options})[5:]
    )
    # TODO add a slider for the ratings
    # allowed_ratings = st.select_slider("Choose range of ratings...", options=[0, 1, 2, 3, 4, 5], value=(0, 5))

    if len(selected_years) == 0:
        selected_years = sorted({x for x in year_options})
    if len(selected_players) == 0:
        selected_players = name_options

    st.header("Rating Reviewer")
    st.write("The column with `Rate` is the ground truth data")
    ignore_not_matches = st.checkbox("Ignore not matched names", value=True)
    prepared_frame = filtered_rating_data(
        rating, selected_players, selected_years, ignore_not_matches
    ).sort_values(by="season", ascending=False).reset_index(drop=True)
    st.dataframe(
        prepared_frame,
        use_container_width=True,
        hide_index=True,
    )


if __name__ == '__main__':
    main()

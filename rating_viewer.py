from typing import List

import pandas as pd
import streamlit as st
import os

from src.utils.database import load_hr, load_all_apba

st.set_page_config(layout="wide")

available_stats = ["Faceoff", "Defence", "Passing"]
ground_truth_data = load_all_apba()
generated_data = {
    "Faceoff": pd.read_csv("data/generated_data/FaceoffRating.csv"),
}

name_options = {f"{first} {last}" for first, last in zip(ground_truth_data["First"], ground_truth_data["Last"])}

year_options = {f"20{year}" for year in ground_truth_data["year"]}


# TODO anononimize the data from both sources so we have better data to work with.
def filtered_rating_data(rating: str, selected_players: List[str], selected_years: List[str]):
    # this below code prepares the apba data for the selected players and years.
    if rating == "Defence":
        defense_rating = [
            max(x) for x in zip(
                ground_truth_data["RateCDefence"].tolist(),
                ground_truth_data["RateRwDefence"].tolist(),
                ground_truth_data["RateLDDefence"].tolist(),
                ground_truth_data["RateRDDefence"].tolist(),
                ground_truth_data["RateLWDefense"].tolist()
            )
        ]
        rating_filtered = ground_truth_data[
            ["First", "Last", "year"]
        ]

        rating_filtered[f"Rate{rating}"] = defense_rating
    else:
        rating_filtered = ground_truth_data[["First", "Last", "year", f"Rate{rating}"]]

    name_filtered = rating_filtered[
        ground_truth_data["First"].str.cat(ground_truth_data["Last"], sep=" ").isin(selected_players)]

    year_filtered = name_filtered[name_filtered["year"].isin([x[2:] for x in selected_years])]

    pd.merge()

    return year_filtered


def main():
    st.title("APBA Rating Demo")

    rating = st.selectbox("Choose a rating...", options=available_stats)

    st.header("Filters")
    selected_players = st.multiselect("Choose a player name...", options=name_options, default="Connor McDavid")
    selected_years = st.multiselect(
        "Choose years...", options=year_options, default=sorted({x for x in year_options})[5:]
    )

    st.header("Ground Truth")

    st.dataframe(
        filtered_rating_data(
            rating, selected_players, selected_years
        ).sort_values(by="year", ascending=False).reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
    )


if __name__ == '__main__':
    main()

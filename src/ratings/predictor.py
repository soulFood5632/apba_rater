import numpy as np

defense_position = ['LD', 'RD', 'D']
forward_position = ['LW', 'RW', 'C', 'W', 'F']


def ci_face_off_rating(games_played: int, facoff_wins: int, faceoff_losses: int):
    """Calculates the face-off rating for a player

    The adjustables values are the constants in the win_comp and
     total_comp equations. These values have been verified
    """

    win_pct = np.divide(facoff_wins, (facoff_wins + faceoff_losses),
                        where=(facoff_wins + faceoff_losses) != 0, out=np.zeros_like(facoff_wins).astype(float))
    fo_total = (facoff_wins + faceoff_losses) * 82 / games_played
    # these constants have been verified through testing. You can see the documentation for example graphs.
    win_comp = 1 / (1 + np.exp(-24.9 * (win_pct - 0.5)))
    total_comp = 1.6 / (1 + np.exp(-0.005 * (fo_total - 250))) - 0.4

    return win_comp * total_comp


def cd_face_off_rating(games_played: int, faceoff_wins: int, faceoff_losses: int, prev_rating: int):
    """Calculates the face-off rating for a player adjusted for previous year rating

    :param: faceoff_wins: The number of faceoffs won
    :param: faceoff_losses: The number of faceoffs lost
    :param: prev_rating: The face-off rating for a player from the previous year

    :returns: The face-off rating for a player adjusted for previous year rating"""
    adjustment_rate = 0.3
    return prev_rating + adjustment_rate * (
            ci_face_off_rating(games_played, faceoff_wins, faceoff_losses) - prev_rating)


def ci_defense_rating(ATOI: int, GA_60: float, GF_60: float, eGA_60: float, eGF_60: float, corsi_a_60: float, d_zone_start: float, position: str, corsi_relative: float):
    """ Caclulates the contex indepedent defence rating for a player

    :param corsi_relative: the relative corsi of the given player
    :param ATOI: The average time on ice in minutes for the player
    :param GA_60: The goals against per 60 minutes for the player
    :param eGA_60: The expected goals against per 60 minutes for the player
    :param d_zone_start: The percentage of defensive zone starts for the player
    :param position: The position of the player. Must be one of 'LD', 'RD', 'D', 'LW', 'RW', 'C', 'W', 'F'

    :returns: The context independent defence rating for a player
    """

    # please refer to jupyter notebook for the data exploration.

    # the logic is as follows:
    # - the players ice time and d_zone_start changes the maximum rating one can have. At the limits of
    # these values for defencemen, 22+ mins per game gives the chance at a 5, and anything below 16 mins
    # gives a maximum of 3.5.
    # - Similarly, 70% defensive zone starts will boost the rating by 0.5 and the
    # 30% will decrease by 0.5.
    # - A GA_60 of 1.5 will yield max rating + 1 and over 3 will yield a min rating
    # - A eGA_60 of 1.75 will yield max rating + 1 and over 2.5 will yield a min rating
    # one other major problem to deal with is how offensive players reduce their time spent in the d-zone.
    # So the rating of ex

    # note that these relationships within the end points are roughly linear. and will capped at the provided limits.

    expected_goals_rating = 1.5 / (1 + np.exp(3 / 0.75 * (eGA_60 - 2.25)))
    goals_against_rating = 1.5 / (1 + np.exp(3 / 1 * (GA_60 - 2.5)))

    expected_goals_rating = expected_goals_rating - 0.4 / (1 + np.exp(5 * (expected_goals_rating - 0.8))) / (1 + np.exp(-2 * (eGF_60 - 3)))
    goals_against_rating = goals_against_rating - 0.4 / (1 + np.exp(5 * (goals_against_rating - 0.8))) / (
                1 + np.exp(-2 * (GF_60 - 3)))
    d_zone_adj = 0.2 / (1 + np.exp(-3 / 20 * (d_zone_start - 50))) - 0.1

    corsi_a_adj = 0.3 / (1 + np.exp(3 / 10 * (corsi_a_60 - 45))) - 0.15

    toi_adj = np.where(np.isin(position, defense_position),
                       0.3 / (1 + np.exp(-3 / 5 * (ATOI / 60.0 - 20))) + 0.81,
                       0.1 / (1 + np.exp(-3 / 3 * (ATOI / 60.0 - 15))) + 0.95)

    corsi_adj = 0.1 / (1 + np.exp(-3 / 5 * corsi_relative)) - 0.05

    # print('expect goals', expected_goals_rating)
    # print('goals against', goals_against_rating)
    # print('d_zone_adj', d_zone_adj)
    # print('corsi_adj', corsi_adj)
    # print('corsi_a_adj', corsi_a_adj)
    # print('toi_adj', toi_adj)

    return toi_adj * (7 * expected_goals_rating + 3 * goals_against_rating) / 10 + d_zone_adj + corsi_adj + corsi_a_adj


def scale_to(input: float, max: int, min: int):
    """ Scales the provided input from 0 to 1 to the provided min and max values

    :param input: The input to be scaled
    :param max: The maximum value of the input
    :param min: The minimum value of the input
    :returns: The scaled value of the input
    """

    def scaler(x):
        return (max - min) * x + min

    return int(round(scaler(input)))

# print(ci_defense_rating(1351, 1.4, 1.75, 41.85, 69.2, 'LD', -3.7))



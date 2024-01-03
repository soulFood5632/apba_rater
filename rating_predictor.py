import numpy as np


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
    return prev_rating + adjustment_rate * (ci_face_off_rating(games_played, faceoff_wins, faceoff_losses) - prev_rating)


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

# print(ci_face_off_rating(0, 0))


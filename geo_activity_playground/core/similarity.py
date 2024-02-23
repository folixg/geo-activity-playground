import collections
import itertools
import pathlib
import pickle

import numpy as np
import pandas as pd
from tqdm import tqdm

from .activities import ActivityRepository
from .coordinates import get_distance


similarity_path = pathlib.Path("Cache/activity_similarity.pickle")


def precompute_activity_distances(repository: ActivityRepository) -> None:
    raw_similarities: dict[tuple[int, int], float] = {}
    near_activities: dict[int, dict[int, float]] = collections.defaultdict(dict)

    if similarity_path.exists():
        with open(similarity_path, "rb") as f:
            raw_similarities, near_activities = pickle.load(f)

    activity_ids = [activity["id"] for activity in repository.iter_activities()]
    missing_pairs = [
        pair
        for pair in itertools.product(activity_ids, activity_ids)
        if pair[0] < pair[1] and not pair in raw_similarities
    ]

    for first_id, second_id in tqdm(missing_pairs, desc="Activity distances"):
        first_activity = repository.get_activity_by_id(first_id)
        second_activity = repository.get_activity_by_id(second_id)

        distance_between_starts = get_distance(
            first_activity["start_latitude"],
            first_activity["start_longitude"],
            second_activity["start_latitude"],
            second_activity["start_longitude"],
        )
        distance_between_ends = get_distance(
            first_activity["end_latitude"],
            first_activity["end_longitude"],
            second_activity["end_latitude"],
            second_activity["end_longitude"],
        )

        if min(distance_between_starts, distance_between_ends) > 200:
            raw_similarities[(first_id, second_id)] = 0
            raw_similarities[(second_id, first_id)] = 0
        else:
            first_ts = repository.get_time_series(first_id)
            second_ts = repository.get_time_series(second_id)
            distance_1 = asymmetric_activity_overlap(first_ts, second_ts)
            distance_2 = asymmetric_activity_overlap(second_ts, first_ts)
            raw_similarities[(first_id, second_id)] = distance_1
            raw_similarities[(second_id, first_id)] = distance_2

            overlap = min(distance_1, distance_2)
            if overlap > 0.9:
                near_activities[first_id][second_id] = overlap
                near_activities[second_id][first_id] = overlap

    with open(similarity_path, "wb") as f:
        pickle.dump((raw_similarities, near_activities), f)


def asymmetric_activity_overlap(
    activity: pd.DataFrame, reference: pd.DataFrame
) -> float:
    sample = activity.iloc[np.linspace(0, len(activity) - 1, 100, dtype=np.int64)]
    min_distances = [
        _get_min_distance(latitude, longitude, reference)
        for (latitude, longitude) in zip(sample["latitude"], sample["longitude"])
    ]
    return sum(distance < 25 for distance in min_distances) / len(min_distances)


def _get_min_distance(latitude: float, longitude: float, other: pd.DataFrame) -> float:
    distances = get_distance(latitude, longitude, other["latitude"], other["longitude"])
    return np.min(distances)

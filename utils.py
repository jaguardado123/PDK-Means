import json
import numpy as np
import matplotlib.pyplot as plt
from kombu.log import get_logger

LOGGER = get_logger(__name__)


class Singleton(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


def dict_upper(data):
    if isinstance(data, dict):
        return {key.upper(): dict_upper(value) for key, value in data.items()}
    else:
        return data


def to_json(data):
    return json.dumps(data, ensure_ascii=False, default=str)


def from_json(data):
    return json.loads(data)


def to_file(data, file):
    return json.dump(data, file, ensure_ascii=False, default=str)


def from_file(file):
    return json.load(file)


def to_format_json(data):
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


def to_format_file(data, file):
    return json.dump(data, file, indent=2, ensure_ascii=False, default=str)


def load_bmi_data(path):
    data = np.loadtxt(path, delimiter=",", dtype=object, skiprows=1)
    data = data[:, 1:3].astype(float)
    return data


def plot(data, centroids, k, d, save=False):
    # setting color values for our
    color = np.random.rand(k + 1, 3)

    for row in data:
        min_distance = float("inf")
        min_centroid = -1

        for i, centroid in enumerate(centroids):
            distance = 0

            for j in range(d):
                distance += (centroid[j] - row[j]) ** 2

            distance = np.sqrt(distance)

            if distance < min_distance:
                min_distance = distance
                min_centroid = i

        plt.scatter(row[0], row[1], c=[color[min_centroid]])

    # plot centroids
    for centroid in centroids:
        plt.scatter(centroid[0], centroid[1], c=[color[k]])

    plt.xlabel("Height/ cm")
    plt.ylabel("Weight/ kg")

    if save:
        plt.savefig("output.png")
    else:
        plt.show()

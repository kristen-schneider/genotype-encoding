# Needs Python >= 3.9
import random
from collections import defaultdict
from typing import Any, Iterable, Mapping, Sequence

import tensorflow as tf

# copied partially from itertools recipes
def grouper(iterable: Iterable, n: int, in_order=True) -> Iterable[tuple[Any, ...]]:
    """
    Collect data into non-overlapping fixed-length chunks or blocks.
    eg: grouper('ABCDEFG', 3) --> ABC DEF

    Note: if n doesn't divide evenly into the length of the iterable,
    the remainder is ommited.

    If in_order is True, return the group in sorted order (ascending).

    """
    if in_order:
        iterable = sorted(iterable)
    args = [iter(iterable)] * n
    return zip(*args)


def sample_without_replacement(n: int) -> list[int]:
    """
    Sample n random numbers without replacement.
    """
    return random.sample(range(n), n)


def sample_pairs(samples: Sequence, distances: Mapping[int, Mapping[int, float]]):
    """
    Yeild random pairs of samples and distances
    - samples: like a list or np array containing the samples
    - distances: two level mapping of sample indices to pairwise distance.
    distances[i][j] is the distance between sample i and sample j.

    Note: I am assuming that i < j.

    Also we are assuming that samples fits into memory.
    """
    for i, j in grouper(sample_without_replacement(len(samples)), 2):
        yield samples[i], samples[j], distances[i][j]


# ------------------------------------------------------------------------------
# Test it out
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # i < j ensures that we dont get redundant pairs i, j and j, i.
    dummy_encodings = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    distances = defaultdict(dict)
    for i in range(10):
        for j in range(10):
            if i < j:
                distances[i][j] = random.random()

    # Sanity check: 10 choose 2 = 45, so there should be 45 possible pairs
    # Sampling from 10 pairs of items without replacement should give us 5 pairs.
    # n = 0
    # for i in distances:
    #     for j in distances[i]:
    #         print(f"{n}: {i=}, {j=}, {distances[i][j]=}")
    #         n += 1

    dataset = tf.data.Dataset.from_generator(
        # the generator has to be callable and take no args
        # that's annoying, but we can wrap the call to sample_pairs in a lambda
        lambda: sample_pairs(dummy_encodings, distances),
        # dtypes of the tensors -- need to adapt to real data
        (tf.int32, tf.int32, tf.float32),
        # shapes of tensors -- need to adapt to real data
        (tf.TensorShape([]), tf.TensorShape([]), tf.TensorShape([])),
    )

    for s1, s2, d in dataset:
        print(f"{s1.numpy() = }, {s2.numpy() = }, {d.numpy() = }")

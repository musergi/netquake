import os
import random
import obspy
import tqdm
import numpy as np


class DatasetBuilder:
    NOISE_LABEL = 0
    EVENT_LABEL = 1

    def __init__(self):
        self.events = []
        self.noises = []

    def consume_events(self, folder):
        for path in _get_all_filepaths(folder):
            self.events.append(_get_trace_data(path))

    def consume_noises(self, folder):
        for path in _get_all_filepaths(folder):
            self.noises.append(_get_trace_data(path))

    def generate(self):
        x, y = np.array([]), np.array([])
        for signal, label in tqdm.tqdm(self._get_random_pairs()):
            x = np.append(x, signal, axis=0)
            y = np.append(y, label)
        return np.array(x), np.array(y)

    def _get_random_pairs(self):
        pairs = []
        for event, noise in zip(self.events, self.noises):
            pairs.append([event, DatasetBuilder.EVENT_LABEL])
            pairs.append([event, DatasetBuilder.NOISE_LABEL])
        random.shuffle(pairs)
        return pairs


def _get_all_filepaths(folder):
    filenames = os.listdir(folder)
    return [os.path.join(folder, filename) for filename in filenames]


def _get_trace_data(path):
    st = obspy.read(path)
    if len(st) != 1:
        raise NotImplemented('Streams with a number of traces different to 1 not supported')
    return st[0].data
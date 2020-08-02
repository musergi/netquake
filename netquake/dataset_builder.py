import os
import obspy
import numpy as np


class DatasetBuilder:
    NOISE_LABEL = 0
    EVENT_LABEL = 1

    def __init__(self):
        self.signals = []
        self.labels = []

    def consume_events(self, folder):
        for path in _get_all_filepaths(folder):
            self.signals.append(_get_trace_data(path))
            self.labels.append(DatasetBuilder.EVENT_LABEL)

    def consume_noises(self, folder):
        for path in _get_all_filepaths(folder):
            self.signals.append(_get_trace_data(path))
            self.labels.append(DatasetBuilder.NOISE_LABEL)

    def generate(self):
        return np.array(self.signals), np.array(self.labels)

    def generate_shuffled(self):
        x, y = self.generate()
        permutation = np.random.permutation(len(x))
        return x[permutation], y[permutation]


def _get_all_filepaths(folder):
    filenames = os.listdir(folder)
    return [os.path.join(folder, filename) for filename in filenames]


def _get_trace_data(path):
    st = obspy.read(path)
    if len(st) != 1:
        raise NotImplemented('Streams with a number of traces different to 1 not supported')
    return st[0].data

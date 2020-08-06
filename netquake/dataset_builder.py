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
        self._make_uniform_length()
        self._balance()
        return np.array(self.signals), np.array(self.labels)

    def _make_uniform_length(self):
        max_shape = max(signal.shape for signal in self.signals)
        for i, signal in enumerate(self.signals):
            if signal.shape[0] != max_shape:
                self.signals[i] = _zero_pad_to_length(signal, max_shape)

    def _balance(self):
        event_indices = np.nonzero(np.array(self.labels) == DatasetBuilder.EVENT_LABEL)[0]
        noise_indices = np.nonzero(np.array(self.labels) == DatasetBuilder.NOISE_LABEL)[0]
        keep_noise_indices = (noise_indices[:len(event_indices)],)
        keep_indices = (np.concatenate((event_indices, keep_noise_indices)),)
        self.signals = np.array(self.signals)[keep_indices]
        self.labels = np.array(self.labels)[keep_indices]

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


def _zero_pad_to_length(trace, shape):
    pad_length = shape[0] - trace.shape[0]
    return np.pad(trace, (0, pad_length), 'constant', constant_values=(0, 0))

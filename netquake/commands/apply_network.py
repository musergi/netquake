import enum
from numpy.core.numeric import roll
import obspy
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model


def initial_zero_padding(arr: np.ndarray, padding: int) -> np.ndarray:
    padded_arr = np.zeros(len(arr) + padding)
    padded_arr[padding:] = arr
    return padded_arr


def smoothed(array, window_size):
    result_length = len(array) - window_size + 1
    result = np.zeros(result_length)
    for i in range(result_length):
        result[i] = np.mean(array[i:i + window_size])
    return result


def rolling_window(a, window, step_size):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1 - step_size + 1, window)
    strides = a.strides + (a.strides[-1] * step_size,)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def run(network_path, trace_path):
    trace = obspy.read(trace_path)[0]
    model = load_model(network_path)

    rolled = rolling_window(trace.data, 3001, 1)
    rolled = np.reshape(rolled, (rolled.shape[0],) + model.layers[0].input_shape[1:])

    result = model.predict(rolled)
    result = np.reshape(result, result.shape[:-1])
    result = initial_zero_padding(result, len(trace.data) - len(result))

    plots = [trace.data]
    plots.append(result)
    plots.append(smoothed(initial_zero_padding(result, 16), 16))
    plots.append(smoothed(initial_zero_padding(result, 64), 64))

    for index, data in enumerate(plots):
        plt.subplot(len(plots), 1, index + 1)
        plt.plot(data)
    plt.show()

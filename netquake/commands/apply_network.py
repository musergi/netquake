import obspy
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model


def rolling_window(a, window, step_size):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1 - step_size + 1, window)
    strides = a.strides + (a.strides[-1] * step_size,)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def run(network_path, trace_path):
    trace = obspy.read(trace_path)[0]
    model = load_model(network_path)
    print('InputShape', model.layers[0].input_shape)

    print('Data shape', trace.data.shape)
    rolled = rolling_window(trace.data, 3001, 1)
    rolled = np.reshape(rolled, (rolled.shape[0],) + model.layers[0].input_shape[1:])
    print('Rolled data shape', rolled.shape)

    result = model.predict(rolled)
    print('Result shape', result.shape)
    result = np.reshape(result, result.shape[:-1])

    plt.subplot(2, 1, 1)
    plt.plot(trace.data)
    plt.subplot(2, 1, 2)
    plt.plot(result)
    plt.show()

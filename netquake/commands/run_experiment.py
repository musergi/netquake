import json
import pickle
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Model, model_from_json
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.callbacks import Callback


class ReportCallback(Callback):
    def __init__(self, dump_list):
        self.dump_list = dump_list

    def on_epoch_end(self, epoch, logs=None):
        self.dump_list.append({'epoch':epoch, **logs})


class ExperimentRunner:
    def __init__(self, config_path, model_path):
        self._parse_config(config_path)
        self.model = model_from_json(model_path)
        self._compile_model()

    def _parse_config(self, path):
        with open(path) as config_file:
            config = json.load(config_file)
            self.dataset_path = config['dataset_path']
            self.epochs = config['epochs']

    def _compile_model(self):
        self.model.compile(
            optimizer=Adam(),
            loss=BinaryCrossentropy(),
            metrics=['accuracy', tf.math.confusion_matrix]
        )

    def run(self):
        dataset = None
        with open(self.dataset_path, 'rb') as dataset_file:
            dataset = pickle.load(dataset_file)
        reports = []
        self.model.fit(
            *dataset,
            batch_size=1,
            epochs=self.epochs,
            callbacks=[ReportCallback(reports)]
        )
        return pd.DataFrame(reports)

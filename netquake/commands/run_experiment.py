import json
import pickle
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import model_from_json
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.metrics import TruePositives, TrueNegatives, FalsePositives, FalseNegatives


class ReportCallback(Callback):
    def __init__(self):
        self.dump_list = []

    def on_epoch_end(self, epoch, logs=None):
        self.dump_list.append({'epoch': epoch, **logs})

    def get_dataframe(self):
        return pd.DataFrame(self.dump_list)


class ExperimentRunner:
    def __init__(self, config_path, model_path):
        self._parse_config(config_path)
        with open(model_path) as model_file:
            self.model = model_from_json(model_file.read())
        self._compile_model()

    def _parse_config(self, path):
        with open(path) as config_file:
            config = json.load(config_file)
            self.dataset_path = config['dataset_path']
            self.epochs = config['epochs']
            self.dump_path = config['result_path']
            self.net_save_path = config['network_path']

    def _compile_model(self):
        self.model.compile(
            optimizer=Adam(),
            loss=BinaryCrossentropy(),
            metrics=['accuracy', TruePositives(), TrueNegatives(), FalsePositives(), FalseNegatives()]
        )
        self.model.summary()

    def run(self):
        dataset = None
        with open(self.dataset_path, 'rb') as dataset_file:
            dataset = pickle.load(dataset_file)
        reports = ReportCallback()
        self.model.fit(
            *dataset,
            batch_size=1,
            epochs=self.epochs,
            validation_split=0.1,
            callbacks=[reports]
        )
        self.model.save(self.net_save_path)
        reports.get_dataframe().to_csv(self.dump_path)


def run(config, model):
    experiment_runner = ExperimentRunner(
        config_path=config,
        model_path=model
    )
    experiment_runner.run()
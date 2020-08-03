import unittest
import pandas as pd
from netquake.commands.run_experiment import ExperimentRunner


TEST_CONFIG = 'inputs/test_config.json'


class ExperimentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.experiment_runner = ExperimentRunner(config_path=TEST_CONFIG)

    def test_running(self):
        results = self.experiment_runner.run()
        self.assertIsNotNone(results)
        self.assertIsInstance(results, pd.DataFrame)
        self.assertGreater(len(results), 0)
        for field in ['epoch', 'acc', 'loss', 'val_acc', 'val_loss']:
            self.assertIn(field, results)


if __name__ == '__main__':
    unittest.main()

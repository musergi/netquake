import unittest
import os
from netquake.dataset_builder import DatasetBuilder


EVENT_FOLDER = 'inputs/windows/event'
NOISE_FOLDER = 'inputs/windows/noise'


class DatasetBuilderTester(unittest.TestCase):
    def setUp(self) -> None:
        self.dataset_builder = DatasetBuilder()

    def test_event_consumption(self):
        self.dataset_builder.consume_events(EVENT_FOLDER)
        self.assertEqual(len(self.dataset_builder.signals), len(os.listdir(EVENT_FOLDER)))

    def test_noise_consumption(self):
        self.dataset_builder.consume_noises(NOISE_FOLDER)
        self.assertEqual(len(self.dataset_builder.signals), len(os.listdir(NOISE_FOLDER)))

    def test_dataset_generation(self):
        self.dataset_builder.consume_events(EVENT_FOLDER)
        self.dataset_builder.consume_noises(NOISE_FOLDER)
        x, y = self.dataset_builder.generate()
        projected_size = len(os.listdir(EVENT_FOLDER)) + len(os.listdir(NOISE_FOLDER))
        self.assertEqual(x.shape, (projected_size, 3001))

    def test_dataset_shuffling(self):
        self.dataset_builder.consume_events(EVENT_FOLDER)
        self.dataset_builder.consume_noises(NOISE_FOLDER)
        x1, _ = self.dataset_builder.generate()
        x2, _ = self.dataset_builder.generate_shuffled()
        self.assertEqual(x1.shape, x2.shape)


if __name__ == '__main__':
    unittest.main()
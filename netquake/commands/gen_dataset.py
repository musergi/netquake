import os
import pickle
from netquake.dataset_builder import DatasetBuilder


NOISE_LABEL = 0
EVENT_LABEL = 1


def parse_args(args):
    return args[1:], args[0]


def run(*args):
    input_dirs, output_path = parse_args(args)
    dataset_builder = DatasetBuilder()
    for input_dir in input_dirs:
        dataset_builder.consume_events(os.path.join(input_dir, 'event'))
        dataset_builder.consume_noises(os.path.join(input_dir, 'noise'))
    with open(output_path, 'wb') as out_file:
        pickle.dump(dataset_builder.generate(), out_file)

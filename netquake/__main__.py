import argparse
import importlib


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', type=str, default=None)
    parser.add_argument('--input', nargs='+')
    parser.add_argument('--output', nargs='+')
    args = parser.parse_args()

    lib = importlib.import_module(f'netquake.commands.{args.command}')
    lib.run(args.input, args.output)
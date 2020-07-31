import os
import tqdm
from obspy.core import stream
from netquake.trace import WindowWriter
from netquake.catalog import Catalog


def run(inputs, outputs):
	catalog_path, signal_folder, window_size, event_start_offset = inputs
	folder = outputs[0]

	window_writer = WindowWriter(
		folder=folder,
		window_size=window_size,
		event_start_offset=event_start_offset)

	catalog = Catalog.from_csv(catalog_path)

	for signal_filename in tqdm.tqdm(os.listdir(signal_folder)):
		# Read stream
		st = stream.read(os.path.join(signal_folder, signal_filename))
		# Streams are expected to only have one trace if they have multiple only the first one is used
		trace = st[0]
		window_writer.write_windows(trace, catalog)

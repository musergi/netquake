import os
import tqdm
import pandas as pd
from obspy.core import stream
from netquake.catalog import Catalog
from netquake.trace import TraceWriter
from netquake.trace import get_trace_component


def run(inputs, outputs):
	catalog_filepath, signals_folder = inputs
	dump_folder = outputs[0]

	catalog = Catalog.from_csv(catalog_filepath)
	trace_writer = TraceWriter(dump_folder)

	for filename in tqdm.tqdm(os.listdir(signals_folder)):
		file_stream = stream.read(os.path.join(signals_folder, filename))
		for trace in file_stream:
			if get_trace_component(trace) != 'Z':
				continue
			if len(catalog.get_trace_picks(trace)) > 0:
				trace_writer.write(trace)

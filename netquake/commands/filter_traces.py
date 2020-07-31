import os
import tqdm
from obspy.core import stream
from netquake.catalog import Catalog
from netquake.trace import TraceWriter
from netquake.trace import get_trace_component


def run(catalog_path, trace_folder, dump_folder):
	catalog = Catalog.from_csv(catalog_path)
	trace_writer = TraceWriter(dump_folder)

	for filename in tqdm.tqdm(os.listdir(trace_folder)):
		file_stream = stream.read(os.path.join(trace_folder, filename))
		for trace in file_stream:
			if get_trace_component(trace) != 'Z':
				continue
			if len(catalog.get_trace_picks(trace)) > 0:
				trace_writer.write(trace)

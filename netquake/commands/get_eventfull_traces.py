import os
import tqdm
import pandas as pd
from obspy.core import stream


class TraceWriter:
    def __init__(self, folder:str):
        self.index = 0
        self.folder = folder

    def _get_unique_filepath(trace):
    	station_code = trace.stats.stats.station
    	channel_code = trace.stats.channel
    	filename = f'{station_code}_{channel_code}_{self.index}.mseed'
    	self.index += 1
    	return os.path.join(self.folder, filename)

    def write_trace(trace):
    	trace.write(self._get_unique_filepath(trace))


def _contains_event(trace, df):
    station_code = trace.stats.station
    channel_code = trace.stats.channel[1:]
    start = trace.stats.starttime
    end = trace.stats.endtime
    possible_picks = df[
        (df['station_code'] == station_code) &
        (df['channel_code'] == channel_code) &
        (df['time'] > start) &
        (df['time'] < end)]
    return len(possible_picks) > 0

def run(inputs, outputs):
    catalog_filepath, signals_folder = inputs
    dump_folder = next(outputs)

    df = pd.read_csv(catalog_filepath)
    trace_writer = TraceWriter(dump_folder)

    for filename in tqdm.tqdm(os.listdir(signals_folder)):
        file_stream = stream.read(os.path.join(signals_folder, filename))
        for trace in file_stream:
            if _contains_event(trace, df):
                trace_writer.write(trace)

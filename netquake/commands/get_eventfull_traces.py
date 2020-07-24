import os
import tqdm
import pandas as pd
from obspy.core import stream

def contains_event(trace, df):
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

def run(input_paths, output_paths):
    df = pd.read_csv(input_paths[0])
    signals_folder = input_paths[1]
    dump_folder = output_paths[0]
    
    index = 0
    for filename in tqdm.tqdm(os.listdir(signals_folder)):
        file_stream = stream.read(os.path.join(signals_folder, filename))
        for trace in file_stream:
            if contains_event(trace, df):
                trace.write(os.path.join(dump_folder, f'{index}.mseed'), format='MSEED')
                index += 1

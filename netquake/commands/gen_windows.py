import os
import datetime as dt
import tqdm
import pandas as pd
from obspy.core import stream
from obspy.core.utcdatetime import UTCDateTime

def run(inputs, outputs):
    # Get input paths
    catalog_path = inputs[0]
    signal_folder = inputs[1]

    # Get parameters
    window_size = int(inputs[2])
    event_start_offset = float(inputs[3])

    # Get ouput directories
    dump_folder = outputs[0]
    event_folder = os.path.join(dump_folder, 'event')
    noise_folder = os.path.join(dump_folder, 'noise')

    # Make output directories
    os.makedirs(event_folder, exist_ok=True)
    os.makedirs(noise_folder, exist_ok=True)

    # Load catalog
    df = pd.read_csv(catalog_path)

    # Filter only Z picks for faster lookups
    df = df[df['channel_code'].str.contains('Z')]

    # Iterate over all the signals
    for signal_filename in tqdm.tqdm(os.listdir(signal_folder)):
        # Read stream
        st = stream.read(os.path.join(signal_folder, signal_filename))

        # Streams are expected to only have one trace if they have multiple only the first one is used
        trace = st[0]

        # Check if it is not the Z components
        if trace.stats.channel[2] != 'Z':
            continue
        
        # Get relevant picks
        station_code = trace.stats.station
        channel_code = trace.stats.channel[1:]
        start = trace.stats.starttime
        end = trace.stats.endtime
        window_picks = df[
            (df['station_code'] == station_code) &
            (df['channel_code'] == channel_code) &
            (df['time'] > start) &
            (df['time'] < end)]
        
        # Check if no picks are found or if more than 1 pick is found
        if len(window_picks) != 1:
            print(f'Not handled case for {len(window_picks)} picks.')
            continue

        # Get signal internal id
        signal_id = signal_filename.split('.')[0]
        
        # Get pick time
        pick_time = UTCDateTime(pd.to_datetime(window_picks.iloc[0]['time'], utc=True))
        
        event_start = pick_time - window_size * event_start_offset
        event_end = event_start + window_size

        event_slice = trace.slice(event_start, event_end)
        event_slice.write(os.path.join(event_folder, f'{signal_id}_0.mseed'))

        noise_start = event_start - window_size
        index = 1
        while noise_start > start:
            noise_slice = trace.slice(noise_start, noise_start + window_size)
            noise_slice = trace.write(os.path.join(noise_folder, f'{signal_id}_{index}.mseed'))

            noise_start -= window_size
            index += 1

import os
import datetime as dt
import tqdm
import pandas as pd
from obspy.core import stream
from obspy.core.utcdatetime import UTCDateTime


class WindowWriter:
    def __init__(self, dump_folder, window_size, event_start_offset):
        self.noise_index = 0
        self.event_index = 0
        self.window_size = window_size
        self.event_start_offset = event_start_offset
        self.event_folder = os.path.join(dump_folder, 'event')
        self.noise_folder = os.path.join(dump_folder, 'noise')

        os.makedirs(self.event_folder, exist_ok=True)
        os.makedirs(self.noise_folder, exist_ok=True)

    def write_windows(self, trace, catalog):
        pick_time = _get_pick_in_trace(trace, catalog)
        event_window_start = self._get_event_window_start(pick_time)
        noise_windows_start = self._get_noise_windows_start(
            event_window_start, trace)
        self._write_event_window(trace, event_window_start)
        for noise_window_start in noise_windows_start:
            self._write_noise_window(noise_window_start)

    def _get_event_window_start(self, pick_time:UTCDateTime) -> UTCDateTime:
        time_offset = self.window_size * self.event_start_offset
        return pick_time - time_offset

    def _get_noise_windows_start(self, event_window_start:UTCDateTime, trace):
        window_starts = []
        noise_start = event_window_start - self.window_size
        while noise_start > trace.stats.starttime:
            window_starts.append(noise_start)
            noise_start -= self.window_size
        return window_starts

    def _write_event_window(self, trace, starttime):
        sub_trace = trace.slice(starttime, starttime + self.window_size)
        sub_trace.write(self._get_event_window_filepath(trace))

    def _get_event_window_filepath(self, trace):
        station = trace.stats.stats.station
        channel = trace.stats.channel
        filename = f'{station}_{channel}_event_{self.event_index:05d}.mseed'
        self.event_index += 1
        return os.path.join(self.event_folder, filename)

    def _write_noise_window(self, trace, starttime):
        sub_trace = trace.slice(starttime, starttime + self.window_size)
        sub_trace.write(self._get_noise_window_filepath(trace))

    def _get_noise_window_filepath(self, trace, starttime):
        station = trace.stats.stats.station
        channel = trace.stats.channel
        filename = f'{station}_{channel}_noise_{self.noise_index:05d}.mseed'
        self.noise_index += 1
        return os.path.join(self.noise_folder, filename)


def _get_pick_in_trace(trace, catalog) -> UTCDateTime:
    station_code = trace.stats.station
    channel_code = trace.stats.channel[1:]
    start = trace.stats.starttime
    end = trace.stats.endtime
    picks = catalog[
        (catalog['station_code'] == station_code) &
        (catalog['channel_code'] == channel_code) &
        (catalog['time'] > start) &
        (catalog['time'] < end)]

    if len(picks) != 1:
        raise NotImplementedError('Found trace with more than one pick or none!')

    pick_time = UTCDateTime(pd.to_datetime(window_picks.iloc[0]['time'], utc=True))
    return pick_time


def _parse_input(catalog_path, signal_folder, window_size, event_start_offset):
    return catalog_path, signal_folder, int(window_size), float(event_start_offset)


def run(inputs, outputs):
    catalog_path, signal_folder, window_size, event_start_offset = _parse_input(*inputs)
    dump_folder = outputs[0]

    window_writer = WindowWriter(
        dump_folder=dump_folder,
        window_size=window_size,
        event_start_offset=event_start_offset)

    df = pd.read_csv(catalog_path)
    # Filter only Z picks for faster lookups
    df = df[df['channel_code'].str.contains('Z')]

    for signal_filename in tqdm.tqdm(os.listdir(signal_folder)):
        # Read stream
        st = stream.read(os.path.join(signal_folder, signal_filename))
        # Streams are expected to only have one trace if they have multiple only the first one is used
        trace = st[0]
        # Check if it is not the Z components
        if trace.stats.channel[2] != 'Z':
            continue
        
        window_writer.write_windows(trace, df)

import pandas as pd
from obspy.core.trace import Trace
from obspy.io.nordic.core import read_nordic


class Catalog:
    def __init__(self, df:pd.DataFrame):
        self.df = df

    def filter_inplace(self, func):
        self.df = func(self.df)

    def get_trace_picks(self, trace:Trace):
        station = trace.stats.station
        channel = trace.stats.channel[1:]
        start = trace.stats.starttime
        end = trace.stats.endtime
        return self.df[
            (self.df['station'] == station) &
            (self.df['channel'] == channel) &
            (self.df['time'] > start) &
            (self.df['time'] < end)]

    def to_csv(self, filepath:str):
        self.df.to_csv(filepath)

    @staticmethod
    def from_csv(filepath:str):
        df = pd.read_csv(filepath)
        return Catalog(df)

    @staticmethod
    def from_nordic(filepath:str):
        df = _parse_nordic(filepath)
        return Catalog(df)


def _parse_nordic(filepath:str):
    catalog = read_nordic(filepath)
    picks = {}
    for col in ('magnitud', 'time', 'network', 'station', 'channel'):
        picks[col] = list()
    for event in catalog:
        magnitud = _get_magnitude(event)
        for pick in event.picks:
            picks['magnitud'].append(magnitud)
            picks['time'].append(pick.time)
            picks['network'].append(pick.waveform_id.network_code)
            picks['station'].append(pick.waveform_id.station_code)
            picks['channel'].append(pick.waveform_id.channel_code)
    return pd.DataFrame(picks)


def _get_magnitude(event):
    if event.magnitudes:
        return event.magnitudes[0].mag
    return None

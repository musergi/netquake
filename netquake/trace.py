import os
import pandas as pd
from obspy.core.trace import Trace
from obspy.core.utcdatetime import UTCDateTime
from netquake.catalog import Catalog


class TraceWriter:
	def __init__(self, folder):
		self.index = 0
		self.folder = folder
		os.makedirs(self.folder, exist_ok=True)

	def write(self, trace:Trace):
		trace.write(self._get_unique_filepath(trace))

	def _get_unique_filepath(self, trace:Trace):
		station = trace.stats.station
		channel = trace.stats.channel
		filename = f'{self.index:05d}_{station}_{channel}.mseed'
		self.index += 1
		return os.path.join(self.folder, filename)


class WindowWriter:
	def __init__(self, folder, window_size, event_start_offset):
		self.noise_writer = TraceWriter(os.path.join(folder, 'noise'))
		self.event_writer = TraceWriter(os.path.join(folder, 'event'))
		self.window_size = int(window_size)
		self.event_start_offset = float(event_start_offset)

	def write_windows(self, trace, catalog:Catalog):
		trace.normalize()
		pick_times = _get_picks_in_trace(trace, catalog)
		event_window_starts = [self._get_event_window_start(pick_time) for pick_time in pick_times]
		noise_window_starts = self._get_noise_windows_start(min(event_window_starts), trace)
		self._write_event_windows(trace, event_window_starts)
		self._write_noise_windows(trace, noise_window_starts)

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

	def _write_event_windows(self, trace, starttimes):
		for starttime in starttimes:
			sub_trace = trace.slice(starttime, starttime + self.window_size)
			self.event_writer.write(sub_trace)

	def _write_noise_windows(self, trace, starttimes):
		for starttime in starttimes:
			sub_trace = trace.slice(starttime, starttime + self.window_size)
			self.noise_writer.write(sub_trace)


def get_trace_component(trace: Trace):
	return trace.stats.channel[2]

def _get_pick_in_trace(trace, catalog:Catalog) -> UTCDateTime:
	picks = catalog.get_trace_picks(trace)
	if len(picks) != 1:
		# TODO: Fix
		raise NotImplementedError('Found trace with more than one pick or none!')
		#print(f'Found trace with more than one pick or none! {len(picks)}')

	pick_time = UTCDateTime(pd.to_datetime(picks.iloc[0]['time'], utc=True))
	return pick_time

def _get_picks_in_trace(trace, catalog:Catalog) -> list:
	times = []
	picks = catalog.get_trace_picks(trace)
	for pick in picks.itertuples():
		times.append(UTCDateTime(pd.to_datetime(pick.time, utc=True)))
	return times
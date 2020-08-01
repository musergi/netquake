import os
from obspy import read
from netquake.trace import TraceWriter


def run(input_folder, output_folder, min_freq, max_freq):
    trace_writer = TraceWriter(output_folder)
    for filename in os.listdir(input_folder):
        filepath = os.path.join(input_folder, filename)
        stream = read(filepath)
        for trace in stream:
            trace.filter('bandpass', freqmin=float(min_freq), freqmax=float(max_freq))
            trace.normalize()
            trace_writer.write(trace)

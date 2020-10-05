# Netquake
## Usage

The first step is to take the event catalog, take all the picks from it associated with the Z component, and save them in a simpler CSV format:
```bash
python -m netquake parse_catalog <input-nordic-path> <output-csv-path>
```

The second step is to only take the traces containing events and corresponding to the Z component:
```bash
python -m netquake filter_traces <input-csv-catalog-path> <trace-folder-path> <output-folder-path>
```

The third step is to adapt the traces so they can have an easier input for the neural network, this involves applying a bandpass filter and normalizing the signals. Frequencies are passed in Hertz:
```bash
python -m netquake adapt_traces <trace-folder-path> <output-folder-path> <band-min-freq> <band-max-freq>
```

The fourth step is to slice into windows and save them on different folders if they contain an event or not:
```bash
python -m netquake gen_windows <catalog-path> <eventfull-trace-folder-path> <destination-folder> <window-size-seconds> <event-position>
```

The fifth step is to pack all the datasets into a pickle:
```bash
python -m netquake gen_dataset <output-pickle-path> <trace-folder-paths>
```

For viewing the signals:
```bash
python -m netquake display_traces <trace-folder-path> <trace-count>
```

To train a network:
```bash
python -m netquake run_experiment <config-json-file> <network-json-file>
```

To use a trained network:
```bash
python -m netquake apply_network <network-h5-file> <filtered-mseed-file>
```
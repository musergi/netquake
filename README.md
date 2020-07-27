# Netquake
## Datasets
## Usage

In order to parse the nordic catalog we run the command:
```bash
python -m netquake parse_catalog --input <path-to-nordic-file> --output <output-file-path>
```

In order to filter the traces to only get the ones containing events:
```bash
python -m netquake get_eventfull_traces --input <path-to-csv-catalog> <path-to-trace-folder> --output <dump-folder-path>
```

In order to slice into windows and save them on different folders if they contain an event or not:
```bash
python -m netquake gen_windows --input <catalog-path> <eventfull-trace-folder-path> <window-size-seconds> <event-position> --output <destination-folder>
```

import logging
import tqdm
import pandas as pd
from obspy.io.nordic.core import read_nordic


def run(input_path, output_path):
    catalog = read_catalog(input_path)
    data = {'magnitud': [], 'time': [], 'network_code':[], 'station_code':[], 'channel_code':[]}
    for event in tqdm.tqdm(catalog):
        magnitud = event.magnitudes[0].mag if event.magnitudes else None
        for pick in event.picks:
            data['magnitud'].append(magnitud)
            data['time'].append(pick.time)
            data['network_code'].append(pick.waveform_id.network_code)
            data['station_code'].append(pick.waveform_id.station_code)
            data['channel_code'].append(pick.waveform_id.channel_code)
    df = pd.DataFrame(data)
    df.to_csv(output_path)
    

def read_catalog(filepath: str):
    with open(filepath) as catalog_file:
        catalog = read_nordic(catalog_file)
        logging.info(f'Read catalog with {len(catalog)} events.')
        return catalog
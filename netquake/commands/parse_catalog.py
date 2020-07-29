import logging
import tqdm
import pandas as pd
from obspy.io.nordic.core import read_nordic


def run(inputs, outputs):
    catalog = _read_catalog(filepath=inputs[0])
    data = {'magnitud': [], 'time': [], 'network_code':[], 'station_code':[], 'channel_code':[]}
    for event in tqdm.tqdm(catalog):
        magnitud = _get_magnitude(event)
        for pick in event.picks:
            data['magnitud'].append(magnitud)
            data['time'].append(pick.time)
            data['network_code'].append(pick.waveform_id.network_code)
            data['station_code'].append(pick.waveform_id.station_code)
            data['channel_code'].append(pick.waveform_id.channel_code)
    _save_to_csv(data=data, filepath=outputs[0])

def _get_magnitude(event):
    if event.magnitudes:
        return event.magnitudes[0].mag
    return None

def _save_to_csv(data:dict, filepath:str):
    df = pd.DataFrame(data)
    df.to_csv(filepath)

def _read_catalog(filepath: str):
    with open(filepath) as catalog_file:
        catalog = read_nordic(catalog_file)
        logging.info(f'Read catalog with {len(catalog)} events.')
        return catalog

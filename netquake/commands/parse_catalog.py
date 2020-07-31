from netquake.catalog import Catalog


def keep_only_z_picks(df):
	return df[df['channel'].str.contains('Z')]


def run(inputs, outputs):
    catalog = Catalog.from_nordic(filepath=inputs[0])
    catalog.filter_inplace(keep_only_z_picks)
    catalog.to_csv(filepath=outputs[0])
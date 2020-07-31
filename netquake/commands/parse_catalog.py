from netquake.catalog import Catalog


def keep_only_z_picks(df):
    return df[df['channel'].str.contains('Z')]


def run(catalog_path, output_path):
    catalog = Catalog.from_nordic(filepath=catalog_path)
    catalog.filter_inplace(keep_only_z_picks)
    catalog.to_csv(filepath=output_path)

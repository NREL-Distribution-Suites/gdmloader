from gdmloader.constants import GCS_CASE_SOURCE
from gdmloader.source import SystemLoader    

from gdm.distribution import DistributionSystem, CatalogSystem

import fsspec


def test_gcs_interface():
    loader = SystemLoader()
    loader.add_source(GCS_CASE_SOURCE)
    loader.show_sources()
    loader.show_dataset_by_source(GCS_CASE_SOURCE.name)
    loader.load_dataset(
        system_type=DistributionSystem,
        source_name=GCS_CASE_SOURCE.name,
        dataset_name="testcasev1"
    )
    loader.load_dataset(
        system_type=CatalogSystem,
        source_name=GCS_CASE_SOURCE.name,
        dataset_name="gdm_catalog"
    )
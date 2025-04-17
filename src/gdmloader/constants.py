
from gdmloader.source import SourceModel
import fsspec

GDM_CASE_SOURCE = SourceModel(
    fs=fsspec.filesystem("github", org="NREL-Distribution-Suites", repo="gdm-cases", branch="main"),
    name="gdm-cases",
    url="https://github.com/NREL-Distribution-Suites/gdm-cases",
    folder="data",
)

GCS_CASE_SOURCE = SourceModel(
    fs=fsspec.filesystem("gcs"),
    name="gdm_data",
    url="https://storage.googleapis.com/gdm_data",
    folder="data",
)
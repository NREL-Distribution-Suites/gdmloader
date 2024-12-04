
from gdmloader.source import SourceModel
import fsspec

GDM_CASE_SOURCE = SourceModel(
    fs=fsspec.filesystem("github", org="NREL-Distribution-Suites", repo="gdm-cases", branch="main"),
    name="gdm-cases",
    url="https://github.com/NREL-Distribution-Suites/gdm-cases",
    folder="data",
)
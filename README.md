# Grid Data Model's System Loader

A lightweight package to load [Grid Data Model's](https://github.com/NREL-Distribution-Suites/grid-data-models) systems from a remote location.

## Installation

```bash
pip install gdmloader
```

## Usage

Construct a loader and add a source.

```python
from gdmloader.source import SystemLoader
from from gdmloader.constants import GCS_CASE_SOURCE

loader = SystemLoader()
loader.add_source(GCS_CASE_SOURCE)
```

Show sources.

```python
loader.show_sources()
```

Show the dataset by sources.

```python
loader.show_dataset_by_source(GCS_CASE_SOURCE.name)
```

Load the dataset.

```python
from gdm import DistributionSystem
loader.load_dataset(
    system_type=DistributionSystem,
    source_name=GCS_CASE_SOURCE.name,
    dataset_name="testcasev1"
)
```

If you want to force download a specific version, then you can do this.

```python
from gdm import DistributionSystem
loader.load_dataset(
    system_type=DistributionSystem,
    source_name=GCS_CASE_SOURCE.name,
    dataset_name="testcasev1",
    version="2_0_0"
)
```

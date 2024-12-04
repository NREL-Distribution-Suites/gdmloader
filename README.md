# Grid Data Model's System Loader

A light weight package to load [Grid Data Model's](https://github.com/NREL-Distribution-Suites/grid-data-models) systems from remote location.

## Installation

```bash
pip install gdmloader
```

## Usage

Construct a loader and add a source.

```python
from gdmloader.source import SystemLoader
from from gdmloader.constants import GDM_CASE_SOURCE

loader = SystemLoader()
loader.add_source(GDM_CASE_SOURCE)
```

Show sources.

```python
loader.show_sources()
```

Show dataset by sources.

```python
loader.show_dataset_by_source("gdm-cases")
```

Load dataset.

```python
from gdm import DistributionSystem
loader.load_dataset(
    system_type=DistributionSystem,
    source_name="gdm-cases",
    dataset_name="testcasev1"
)
```

If you want to force download specific version then you can do this.

```python
from gdm import DistributionSystem
loader.load_dataset(
    system_type=DistributionSystem,
    source_name="gdm-cases",
    dataset_name="testcasev1",
    version="1_2_0"
)
```

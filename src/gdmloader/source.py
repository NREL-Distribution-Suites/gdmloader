import json
from os import system
import shutil
import sys
from typing import Type
from pathlib import Path
from typing_extensions import Annotated
import importlib.metadata

from infrasys.system import System
from pydantic import BaseModel, Field
import fsspec
from rich.console import Console
from rich.table import Table


class SourceModel(BaseModel):
    fs: Annotated[
        fsspec.AbstractFileSystem,
        Field(..., description="Filesystem reference."),
    ]
    name: Annotated[str, Field(..., description="Name of the data source")]
    url: Annotated[str | None, Field(..., description="URL of the data source")]
    folder: Annotated[
        str, Field(..., description="Entry folder of the data source")
    ]

    class Config:
        arbitrary_types_allowed = True


def get_gdm_version() -> str:
    return importlib.metadata.version("grid-data-models").replace(".", "_")


class SystemLoader:

    __doc_file_name__ = "doc.json"

    def __init__(self, cached_dir: Path = Path.home() / "gdmloader-cache"):
        self._sources: dict[str, SourceModel] = {}
        self._cached_folder = cached_dir
        if not self._cached_folder.exists():
            self._cached_folder.mkdir()

    def show_sources(self):
        table = Table()
        table.add_column("Name", justify="right", style="cyan", no_wrap=True)
        table.add_column("URL", style="magenta")
        for _, source in self._sources.items():
            table.add_row(source.name, source.url)
        console = Console()
        console.print(table)

    def load_system_doc(self, system_name: str, source_name: str):
        local_doc_file_path = (
            self._cached_folder
            / source_name
            / system_name
            / self.__doc_file_name__
        )
        if not local_doc_file_path.exists():
            source = self._sources[source_name]
            remote_doc_file_path = (
                f"{source_name}/{source.folder}/{system_name}/{self.__doc_file_name__}"
            )
            source.fs.get(remote_doc_file_path, str(local_doc_file_path))
        with open(local_doc_file_path, "r", encoding="utf-8") as fpointer:
            contents = json.load(fpointer)
        return contents

    def show_dataset_by_system(self, system_name: str, source_name: str):
        table = Table(title=f"System: {system_name}")
        doc_contents = self.load_system_doc(system_name, source_name)
        for key in doc_contents[0]:
            table.add_column(key, justify="right", no_wrap=False)
        for item in doc_contents:
            table.add_row(*[str(k) for k in item.values()])
        console = Console()
        console.print(table)

        table = Table(title=f"System: {system_name} versions")
        table.add_column("Version", justify="right", no_wrap=True)
        source = self._sources[source_name]
        for version in source.fs.ls(f"{source_name}/{source.folder}/{system_name}"):
            if version.endswith(".json"):
                continue
            version = Path(version).stem
            table.add_row(version)
        console.print(table)

    def show_dataset_by_source(self, source_name: str):
        source = self._sources[source_name]
        dir_path = f"{source_name}/{source.folder}"
        for system_folder in source.fs.ls(dir_path):
            system_name = Path(system_folder).stem
            self.show_dataset_by_system(system_name, source_name)

    def load_dataset(
        self,
        system_type: Type[System],
        source_name: str,
        dataset_name: str,
        version: str | None = None,
    ):
        if version is None:
            version = get_gdm_version()
        source = self._sources[source_name]
        if source is None:
            raise ValueError(f"Source {source_name} not found")
        remote_folder = f"{source_name}/{source.folder}/{system_type.__name__}/{version}/{dataset_name}"
        local_folder = self._cached_folder / source_name / system_type.__name__ / version
        if not local_folder.exists():
            local_folder.mkdir(parents=True)

        dataset_folder = local_folder / dataset_name
        if not dataset_folder.exists():
            try:
                source.fs.get(
                    remote_folder,
                    str(local_folder),
                    recursive=True,
                )
            except FileNotFoundError:
                msg = f"{remote_folder=} not found! Check the URL: {source.url}/{remote_folder}"
                raise ValueError(msg)

        system_file = list(dataset_folder.rglob("*.json"))[0]
        return system_type.from_json(system_file)

    def invalidate_cache(self):
        if self._cached_folder.exists():
            shutil.rmtree(self._cached_folder)

    def add_source(self, source: SourceModel):
        if source.name in self._sources:
            raise ValueError(f"Source {source.name} already exists")
        self._sources[source.name] = source

    def remove_source(self, source_name: str):
        if source_name not in self._sources:
            raise ValueError(f"Source {source_name} not found")
        self._sources.pop(source_name)

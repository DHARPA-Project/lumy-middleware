import json
import os
from pathlib import Path
from typing import Iterator

from appdirs import user_data_dir
from lumy_middleware.types import WorkflowListItem, LumyWorkflow
from lumy_middleware.utils.dataclasses import from_dict, from_yaml
from lumy_middleware import workflows as workflows_pkg

APP_NAME = 'Lumy'


def load_lumy_workflow_from_file(path: Path) -> LumyWorkflow:
    if path.suffix in ['.yml', '.yaml']:
        return from_yaml(LumyWorkflow, path.read_text())
    return from_dict(LumyWorkflow, json.loads(path.read_text()))


def get_workflow_dir() -> Path:
    '''
    Returns directory where workflow files are stored.

    **NOTE** Workflow directory can be overridden via an
    environmental variable. This is used for unit tests.
    '''
    override_path = os.environ.get('LUMY_WORKFLOW_DIR')
    if override_path is not None:
        path = Path(override_path)
        if path.is_dir():
            return path
    return Path(user_data_dir(appname=APP_NAME)) / 'workflows'


def get_user_workflows(
    include_body: bool
) -> Iterator[WorkflowListItem]:
    if get_workflow_dir().exists():
        for filepath in get_workflow_dir().iterdir():
            if filepath.is_file():
                workflow = load_lumy_workflow_from_file(filepath)
                yield WorkflowListItem(
                    uri=str(filepath),
                    name=workflow.meta.label,
                    body=workflow if include_body else None
                )


def get_bundled_workflows(
    include_body: bool
) -> Iterator[WorkflowListItem]:
    loc = Path(workflows_pkg.__file__).parent / "resources"
    for filepath in loc.iterdir():
        if filepath.is_file():
            workflow = load_lumy_workflow_from_file(filepath)
            yield WorkflowListItem(
                uri=str(filepath),
                name=workflow.meta.label,
                body=workflow if include_body else None
            )


def get_workflows(
    include_body: bool
) -> Iterator[WorkflowListItem]:
    for i in get_bundled_workflows(include_body):
        yield i
    for i in get_user_workflows(include_body):
        yield i

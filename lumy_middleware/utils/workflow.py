import subprocess
from typing import Iterator, List

from lumy_middleware.types import PackageDependency
from pkg_resources import DistributionNotFound, require


def get_missing_dependencies(
    dependencies: List[PackageDependency]
) -> Iterator[PackageDependency]:
    '''
    Returns an iterator over missing dependencies only.
    '''
    for dependency in dependencies:
        try:
            require(dependency.name)
        except DistributionNotFound:
            yield dependency


def install_dependencies(
    dependencies: List[PackageDependency]
) -> Iterator[PackageDependency]:
    '''
    Returns an iterator over dependencies being installed.
    Dependencies that are already present in the environment
    are skipped.
    '''
    for dependency in get_missing_dependencies(dependencies):
        result = subprocess.run(
            ['python', '-m', 'pip', 'install', dependency.name],
            capture_output=True
        )
        if result.returncode != 0:
            msg = ('Could not install dependency '  # type: ignore
                   f'{dependency.name}: {result.stderr}')
            raise Exception(msg)
        else:
            yield dependency
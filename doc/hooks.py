from ploomberutils.nb import process_readme_md
from pathlib import Path
import shutil
from urllib import request
import zipfile


def config_init(app, config):

    # copy outside the doc folder, otherwise sphinx thinks all those files
    # should be part of the documentation
    projects = Path('../../projects-ploomber/')

    if Path(projects).exists():
        print('Using local copy...')

    else:
        print('Cloning from git...')
        git_clone()
        projects = Path('../../projects-master')

    directories = {
        'parametrized': 'user-guide',
        'sql-templating': 'user-guide',
        'testing': 'user-guide',
        'debugging': 'user-guide',
        'spec-api-python': 'get-started'
    }

    process_readme_md(list(directories), parent_dir=projects)

    for name, target_dir in directories.items():
        src = Path(projects, name, 'README.ipynb')
        dst = Path(target_dir, f'{name}.ipynb')
        print(f'Copying {src} to {dst}')
        shutil.copy(src, dst)


def git_clone():
    url = 'https://github.com/ploomber/projects/archive/master.zip'
    request.urlretrieve(url, '../../master.zip')

    with zipfile.ZipFile('../../master.zip', 'r') as f:
        f.extractall('../../')


if __name__ == '__main__':
    config_init(app=None, config=None)

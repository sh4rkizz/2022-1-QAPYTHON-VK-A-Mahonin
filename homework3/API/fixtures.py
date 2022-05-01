import os
import random
import string

import pytest


@pytest.fixture(scope='function')
def photo_path(repo_root) -> str:
    return os.path.join(repo_root, 'API', 'cute_kitten.png')


@pytest.fixture(scope='function')
def randomize_name(length=15) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

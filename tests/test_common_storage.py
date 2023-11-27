###############################################################################
#  test_common_storage.py for archivist stacks microservice                   #
#  Copyright (c) 2023 Tom Hartman (thomas.lees.hartman@gmail.com)             #
#                                                                             #
#  This program is free software; you can redistribute it and/or              #
#  modify it under the terms of the GNU General Public License                #
#  as published by the Free Software Foundation; either version 2             #
#  of the License, or the License, or (at your option) any later              #
#  version.                                                                   #
#                                                                             #
#  This program is distributed in the hope that it will be useful,            #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#  GNU General Public License for more details.                               #
###############################################################################

# Commentary {{{
"""Unit tests for common storage functions."""
# test_common_storage }}}

#  {{{
import os
import shutil
import random
from pathlib import Path
import pytest
from pydantic import DirectoryPath
from app.common import Config, Storage


@pytest.fixture(scope='function', name='test_config')
def fixture_test_client():
    """Testing fixture for storage function unit tests."""

    sandbox = 'tests/sandbox'
    stacks_dir = 'stacks'
    dir_limit = 5
    dir_mask = "{:02d}"

    if os.path.exists(sandbox):
        shutil.rmtree(sandbox)

    os.mkdir(sandbox)
    os.mkdir(DirectoryPath(sandbox, stacks_dir))

    config = Config(storage_root=sandbox,
                    dir_limit=dir_limit,
                    dir_mask=dir_mask,
                    stacks_dir=stacks_dir)

    yield config


def test_storage_path_empty(test_config):
    """
    GIVEN a configured storage location
    WHEN there is no existing directory
    WHEN current_storage_path is called
    THEN should create a new directory starting at 0
    THEN should return the new directory
    """
    storage = Storage(test_config)
    cur_path = storage.current_storage_path()
    stacks_root = DirectoryPath(test_config.storage_root,
                                test_config.stacks_dir)

    assert cur_path.name == '00'
    assert cur_path.exists()
    assert cur_path.parent == stacks_root


def test_storage_path_existing(test_config):
    """
    GIVEN a configured storage location
    WHEN there is an existing directory
    WHEN the folder limit has not been reached
    THEN should return the directory
    """
    storage = Storage(test_config)

    stacks_root = DirectoryPath(test_config.storage_root,
                                test_config.stacks_dir)

    first_dir = DirectoryPath(stacks_root, "00")
    os.mkdir(first_dir)

    cur_path = storage.current_storage_path()
    assert cur_path == first_dir


def test_storage_path_existing_full(test_config):
    """
    GIVEN a configured storage location
    WHEN there is an existing directory
    WHEN the existing directory file count is DIR_LIMIT
    THEN should create next directory
    THEN should return next directory
    """
    storage = Storage(test_config)

    stacks_root = DirectoryPath(test_config.storage_root,
                                test_config.stacks_dir)
    first_dir = DirectoryPath(stacks_root, '00')
    os.mkdir(first_dir)

    for i in range(0, test_config.dir_limit):
        Path(first_dir, f"{i}.txt").touch()

    cur_path = storage.current_storage_path()
    assert cur_path != first_dir
    assert cur_path.name == '01'
    assert cur_path.exists()


def test_storage_multiple_dir(test_config):
    """
    GIVEN a configured storage location
    WHEN there is multiple existing directories
    WHEN the max directory file count is not DIR_LIMIT
    THEN should return the max directory
    """
    storage = Storage(test_config)

    stacks_root = DirectoryPath(test_config.storage_root,
                                test_config.stacks_dir)

    dir_count = random.randint(10, 20)

    for i in range(0, dir_count):
        a_dir = DirectoryPath(stacks_root,
                              test_config.dir_mask.format(i))
        os.mkdir(a_dir)

    cur_path = storage.current_storage_path()
    assert cur_path.name == test_config.dir_mask.format(dir_count-1)

# }}}

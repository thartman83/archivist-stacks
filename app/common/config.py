###############################################################################
#  config.py for archivist stacks                                             #
# Copyright (c) 2023 Tom Hartman (thomas.lees.hartman@gmail.com)              #
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
"""Microservice configuration."""
# }}}

# config {{{

from enum import Enum
from os import environ
from pydantic import DirectoryPath
from pydantic_settings import BaseSettings


def env_or_default(env: str, default: any):
    """Return the value from the environment variable or the default value."""
    return default if env not in environ else environ.get(env)


class Environment(Enum):
    """Microservice environment type."""

    DEV = 1
    TEST = 2
    PROD = 3


class Config(BaseSettings):
    """Microservice Configuration."""

    app_name: str = "Stacks"
    environment: Environment = Environment.DEV

    storage_root: DirectoryPath = env_or_default('STORAGE_ROOT', '/opt/')
    stacks_dir: str = env_or_default('STACKS_PATH', 'stacks')
    dir_limit: int = env_or_default('FOLDER_LIMIT', 500)
    dir_mask: str = env_or_default('FOLDER_MASK', '{:06d}')
    db_url: str = env_or_default('SQL_URL', 'sqlite:///.stacksdb')

# }}}

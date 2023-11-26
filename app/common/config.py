###############################################################################
#  config.py for archivist stacks                                            #
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
from pydantic import BaseModel, FilePath


class Environment(Enum):
    """Microservice environment type."""

    DEV = 1
    TEST = 2
    PROD = 3


class Config(BaseModel):
    """Microservice Configuration."""

    storage_root: FilePath = '/opt/' if 'STORAGE_ROOT' in environ else environ.get('STORAGE_ROOT')
    stacks_path: str = 'stacks' if 'STACKS' in environ else environ.get('STACKS')
    environment: Environment = Environment.DEV
    folder_limit: int = 500 if 'FOLDER_LIMIT' in environ else environ.get('FOLDER_LIMIT')
    folder_mask: str = "{:06d}" if 'FOLDER_MASK' in environ else environ.get('FOLDER_MASK')


config = Config()
# }}}

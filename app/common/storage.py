###############################################################################
#  storage.py for archivist stacks                                            #
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
"""Common storage functions."""
# }}}

# storage {{{
from pydantic import FilePath
from fastapi import UploadFile
from .config import config

stacks_root = FilePath(config.storage_root, config.stacks_path)

# if not stacks_root.exists():
#    stacks_root.mkdir()


def store_record_file(upload_file: UploadFile):
    """Store the upload file into the stacks."""
    pass


def storage_path():
    """Return the storage path."""
    try:
        max_dir = max(stacks_root.iterdir())
        cur_dir = max_dir

        if len([f for f in max_dir.iterdir()]) >= config.folder_limit:
            next_dir = int(cur_dir.name) + 1
            cur_dir = FilePath(stacks_root, config.folder_mask.format(next_dir)).mkdir()
    except:
        pass

    return stacks_root
# }}}

###############################################################################
#  storage.py for archivist stacks                                            #
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
"""Common storage functions."""
# }}}

# storage {{{
import shutil
import uuid
import hashlib
from pathlib import Path
from fastapi import UploadFile
from .config import Config


class Storage():
    """Common storage functions for the stacks microservice."""

    config: Config
    cur_recordid: int = 0

    def __init__(self, config: Config):
        """Construct a new storage object."""
        self.config = config

    def init(self):
        """Initialize the storage structure if not present."""
        storage_root = Path(self.config.storage_root)
        if not storage_root.exists():
            storage_root.mkdir()

        stacks_root = self.stacks_root()
        if not stacks_root.exists():
            stacks_root.mkdir()

    def store_record_file(self, upload_file: UploadFile) -> {Path, str, int}:
        """Store the upload file into the stacks."""
        # read the file to get the checksum, re-seek back to 0 afterwards
        # since we will need to read it again to actually copy the data
        md_hash = hashlib.md5(upload_file.file.read()).hexdigest()
        upload_file.file.seek(0)

        # storage name is a combination of the md checksum and a guid
        # to prevent name collision
        file_storage_name = f"{uuid.uuid4().hex}_{md_hash}"
        destination = Path(self.current_storage_path(), f"{file_storage_name}")

        try:
            with destination.open("wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
        except shutil.Error as err:
            raise err
        finally:
            upload_file.file.close()

        self.cur_recordid = self.cur_recordid + 1
        return (destination, md_hash, self.cur_recordid)

    def current_storage_path(self) -> Path:
        """Return the storage path."""
        dir_mask = self.config.dir_mask
        stacks_root = self.stacks_root()
        max_dir = Path(max(list(stacks_root.iterdir()),
                           default=dir_mask.format(0)))

        if not max_dir.exists():
            max_dir = Path(stacks_root, dir_mask.format(0))
            max_dir.mkdir()
            return max_dir

        count = len(list(max_dir.iterdir()))

        if count >= self.config.dir_limit:
            next_dir = int(max_dir.name) + 1
            max_dir = Path(stacks_root, dir_mask.format(next_dir))
            max_dir.mkdir()

        return max_dir

    def stacks_root(self):
        """Return the root directory for the stacks."""
        return Path(self.config.storage_root, self.config.stacks_dir)
# }}}

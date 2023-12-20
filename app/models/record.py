###############################################################################
#  record.py for Archivist Stacks models                                     #
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
"""Record model."""
# }}}

#  {{{
from datetime import datetime
from pydantic import BaseModel, Field, FilePath


class Record(BaseModel):
    """Record model."""

    id: int
    title: str
    filename: str
    record_path: FilePath
    checksum: str
    size: int
    created: datetime = Field(default=datetime.now())
    modified: datetime = Field(default=datetime.now())

    class Config:  # pylint: disable=too-few-public-methods
        """ORM support for model."""

        orm_mode: True


# }}}

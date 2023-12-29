###############################################################################
#  collection.py for Archivist Stacks models                                  #
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
"""Collection model."""
# }}}

# collection {{{
from typing import List
from pydantic import BaseModel
from app.models import Edition


class CollectionBase(BaseModel):
    """Pydantic representation of a collection base model."""

    title: str


class CollectionCreate(CollectionBase):
    """Pydantic representation of a collection creation model."""

    pass  # pylint: disable=unnecessary-pass


class Collection(BaseModel):
    """Pydantic representation of a collection model."""

    id: int
    editions: List[Edition]
    current_edition: Edition

# }}}

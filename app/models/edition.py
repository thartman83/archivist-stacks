###############################################################################
#  edition.py for Archivist Stacks models                                     #
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
"""Edition model."""
# }}}

# edition {{{
# import hashlib
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from app.models import Record


class EditionBase(BaseModel):
    """Pydantic representation of a edition base model."""

    edition_number: int
    pass  # pylint: disable=unnecessary-pass


class EditionCreate(EditionBase):
    """Pydantic representation of a edition creation model."""

    pass  # pylint: disable=unnecessary-pass


class Edition(EditionBase):
    """Pydantic representation of a edition model."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    native: Record

# }}}

###############################################################################
#  __init__.py for Archivist Stacks database module                           #
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
"""Database module definition."""
# }}}

# __init__ {{{
from .common import get_db, Base, create_tables
from .record_db import RecordDB, create_record
from .edition_db import EditionDB, create_edition
from .collection_db import (
    CollectionDB, create_collection, col_x_ed, find_collection_by_id,
    add_edition
)
__all__ = ['get_db', 'Base', 'create_tables',
           'RecordDB', 'create_record',
           'EditionDB', 'create_edition',
           'CollectionDB', 'create_collection',
           'col_x_ed', 'find_collection_by_id', 'add_edition']

# }}}

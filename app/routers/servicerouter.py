###############################################################################
#  servicerouter.py for archivist stacks                                      #
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
"""General service routes."""
# }}}

# serviceRouter {{{
from fastapi import APIRouter
from app.common import Config, Storage
from app.database import create_tables

ServiceRouter = APIRouter(prefix='/service', tags=['service'])


@ServiceRouter.get('')
def get_service_info():
    """Return general service information."""
    return {
        "configuration": Config().model_dump(),
        "current_storage_dir": Storage(Config()).current_storage_path()
    }


@ServiceRouter.post('/init_db', tags=['service', 'testing'])
def init_db():
    """Initialize the database for testing purposes."""
    create_tables()
    return {
        'Ok': True
    }
# }}}

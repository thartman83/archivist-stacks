###############################################################################
# database.py for archivist stacks                                            #
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
"""Common database functions."""
# }}}

# database {{{
from typing import Any
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.common import Config


def create_dbsession(config: Config) -> {Engine, Session, Any}:
    """Return the engine, local_session and BaseModel for db functions."""
    engine = create_engine(config.db_url)
    local_session = sessionmaker(autocommit=False,
                                 autoflush=False, bind=engine)
    base = declarative_base()

    return (engine, local_session, base)


Engine, Session, DB_Base = create_dbsession(Config())
# }}}

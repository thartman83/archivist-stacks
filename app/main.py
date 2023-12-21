###############################################################################
#  main.py for archivist stacks                                               #
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
"""Stacks main entry point."""
# }}}

# main {{{
from fastapi import FastAPI
from app.common import Config, Engine, DB_Base, Session
from app.routers import RecordRouter, ServiceRouter

__all__ = ['Engine', 'DB_Base', 'Session', 'Config']

app = FastAPI()
app.include_router(RecordRouter)
app.include_router(ServiceRouter)

# }}}

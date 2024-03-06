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
from fastapi.middleware.cors import CORSMiddleware
from app.routers import CollectionRouter, ServiceRouter
# from app.database import get_db, create_tables
# import sqlalchemy as sa

origins = ["*"]

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(CollectionRouter)
app.include_router(ServiceRouter)

# }}}

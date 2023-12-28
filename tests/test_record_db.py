###############################################################################
#  test_record_db.py for Archivist Stacks record_db unit tests                #
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
"""Unit tests for Record_DB."""
# }}}

# test_record_db {{{

import pytest
from sqlalchemy import create_engine, Engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from app.models import Record, RecordCreate
from app.database import Base, create_record

db_url = 'sqlite:///:memory:'
engine: Engine = create_engine(db_url,
                               connect_args={
                                   "check_same_thread": False,
                               },
                               poolclass=StaticPool)


def setup() -> None:
    """Set up the database tables before running tests."""
    Base.metadata.create_all(bind=engine)


def teardown() -> None:
    """Clean up the tables after test completes."""
    # Drop the tables in the test database
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='function', name='TestSessionLocal')
def fixture_test_session() -> Session:
    """Return a sqllite db testing session."""

    testing_session_local = sessionmaker(autocommit=False, autoflush=False,
                                         bind=engine)
    yield testing_session_local


def test_create_record(TestSessionLocal) -> None:
    """Given a stacks database
       WHEN create_record is called
       WHEN parameters are valid
       SHOUL create a database entry for the new record."""

    with TestSessionLocal() as db:
        rec_create = RecordCreate(title='A Title',
                                  filename='afile.docx',
                                  record_path='/opt/storage/localtion/foo.docx',
                                  checksum='alkdsjf2379',
                                  size=12334,
                                  mimetype='application-pdf')
        rec: Record = create_record(rec_create, db)
        assert rec.id is not None

# }}}

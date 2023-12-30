###############################################################################
#  test_collection_db.py for Archivist Stacks unit tests                      #
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
"""Collection ORM database unit tests."""
# }}}

# test_collection_db {{{
import pytest
from sqlalchemy import create_engine, Engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from pydantic import FilePath
from app.models import RecordCreate, CollectionCreate
from app.models import Collection
from app.database import Base, create_collection, add_edition

DB_URL = 'sqlite:///:memory:'
engine: Engine = create_engine(DB_URL,
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


@pytest.fixture(scope='function', name='test_session_local')
def fixture_test_session() -> Session:
    """Return a sqllite db testing session."""

    testing_session_local = sessionmaker(autocommit=False, autoflush=False,
                                         bind=engine)
    yield testing_session_local


def test_create_collection(test_session_local) -> None:
    """
    GIVEN a stacks datebase
    WHEN a collection is create
    SHOULD create a collection, edition, record in the database.
    """

    with test_session_local() as db:
        rec_path = FilePath('LICENSE')
        rec = RecordCreate(title='A Title',
                           filename='afile.docx',
                           record_path=rec_path,
                           checksum='alkdsjf2379',
                           size=12334,
                           mimetype='application-pdf')

        col = CollectionCreate(title='A Title')

        ret: Collection = create_collection(col, rec, db)
        assert ret.id is not None
        assert ret.current_edition.id is not None
        assert ret.current_edition.native.id is not None
        assert len(ret.editions) == 1
        assert ret.editions[0].id == ret.current_edition.id


def test_add_edition(test_session_local) -> None:
    """
    GIVEN a stacks database
    GIVEN a collection exists
    WHEN an edition is added
    SHOULD change the current edition to the new file
    SHOULD have 2 editions in the edition list.
    """

    with test_session_local() as db:
        rec_path = FilePath('tests/testfiles/foo.txt')
        rec = RecordCreate(title='A Title',
                           filename='afile.docx',
                           record_path=rec_path,
                           checksum='alkdsjf2379',
                           size=12334,
                           mimetype='application-pdf')

        col = CollectionCreate(title='A Title')

        ret: Collection = create_collection(col, rec, db)

        rec2_path = FilePath('tests/testfiles/bar.txt')
        rec2 = RecordCreate(title='A Title',
                            filename='afile.docx',
                            record_path=rec2_path,
                            checksum='alkdsjf2379',
                            size=12334,
                            mimetype='text')
        ret2: Collection = add_edition(ret, rec2, db)

        assert ret2.id == ret.id
        assert len(ret2.editions) == 2
        assert ret2.current_edition.id != ret.current_edition.id
        assert ret2.current_edition.native.record_path == rec2_path
# }}}

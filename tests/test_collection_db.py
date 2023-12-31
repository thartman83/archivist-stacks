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
import collections
import pytest
from sqlalchemy import create_engine, Engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from pydantic import FilePath
from app.models import RecordCreate, CollectionCreate
from app.models import Collection
from app.database import (
    Base, create_collection, add_edition, CollectionDB,
    col_x_ed,
    find_edition_by_edition_number, EditionDB
)

SessionCollection = collections.namedtuple('SessionCollection',
                                           'session_local collection_id')

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


@pytest.fixture(scope='function', name='session_collection')
def fixture_test_session_with_data() -> SessionCollection:
    """Return a sqllite db testing session with data."""
    session_local = sessionmaker(autocommit=False, autoflush=False,
                                 bind=engine)

    rec1_path = 'tests/testfiles/foo.txt'
    rec2_path = 'tests/testfiles/bar.txt'
    rec3_path = 'tests/testfiles/baz.txt'

    with session_local() as db:
        col = create_collection(CollectionCreate(
            title='A Collection'
        ), RecordCreate(
            title="A Record",
            record_path=rec1_path,
            filename="ed1.txt",
            checksum="",
            size=123,
            mimetype='application-pdf'
        ), db)

        add_edition(col.id, RecordCreate(
            title="A Second Record",
            record_path=rec2_path,
            filename='ed2.txt',
            checksum="",
            size=123,
            mimetype='application-pdf'
        ), db)

        add_edition(col.id, RecordCreate(
            title="A Third Record",
            record_path=rec3_path,
            filename='ed3.txt',
            checksum="",
            size=123,
            mimetype='application-pdf'
        ), db)

    yield SessionCollection(session_local, col.id)


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
        assert ret.current_edition.edition_number == 0


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
        ret2: Collection = add_edition(ret.id, rec2, db)

        assert ret2.id == ret.id
        assert len(ret2.editions) == 2
        assert ret2.current_edition.id != ret.current_edition.id
        assert ret2.current_edition.native.record_path == rec2_path
        assert ret2.current_edition.edition_number == 1


def test_get_edition_by_edition_number(session_collection) -> None:
    """
    GIVEN a stacks database
    GIVEN a collection with multiple editions
    WHEN get_edition_by_edition_number is invoked
    WHEN collection and edition number is valid
    SHOULD fetch the correct edition
    """

    with session_collection.session_local() as db:
        col_id = session_collection.collection_id

        col = db.query(CollectionDB).filter(CollectionDB.id == col_id).first()

        assert col is not None
        assert len(col.editions) == 3
        assert col.current_edition.edition_number == 2

        ed = find_edition_by_edition_number(col_id, 0, db)
        assert ed is not None
        assert ed.edition_number == 0
        assert ed.native.record_path == FilePath('tests/testfiles/foo.txt')

        ed2 = find_edition_by_edition_number(col_id, 1, db)
        assert ed2 is not None
        assert ed2.edition_number == 1
        assert ed2.native.record_path == FilePath('tests/testfiles/bar.txt')

        ed3 = find_edition_by_edition_number(col_id, 2, db)
        assert ed3 is not None
        assert ed3.edition_number == 2
        assert ed3.native.record_path == FilePath('tests/testfiles/baz.txt')
# }}}

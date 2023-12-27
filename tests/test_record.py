###############################################################################
#  test_record.py for archivist stacks microservice                           #
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
"""Unit tests for record ORM models."""
# }}}

#  {{{
from pathlib import Path
import pytest
import testing.postgresql
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from app.models.record import RecordBase, Record, RecordDB
from app.common import Config
# from app.common.database import create_dbsession


@pytest.fixture(scope='function', name='test_session')
def fixture_test_db():
    """Testing fixture for database connections."""
    cfg = Config()
    name = "testdb"
    port = 5432
    path = "/tmp/my_test_db"

    try:
        cfg.db_url = testing.postgresql.Postgresql(name=name, port=port,
                                                   base_dir=path).url()

        engine: Engine = create_engine(cfg.db_url)
        session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        # engine, session, base = create_dbsession(cfg)

        db: Session = session()
        yield db
    finally:
        db.close()


def test_create_record(test_session):
    """
    GIVEN a
    """

    filepath = "/opt/stacks/000000/arecord.doc"
    Path.touch(filepath)
    rec = RecordBase(title="Arecord", filename="Arecord.doc",
                     record_path=filepath,
                     size=1234, mimetype="application-pdf",
                     checksum="129381238ab")

    rec_db = RecordDB(**rec.model_dump())
    test_session.add(instance=rec_db)
    test_session.commit()
    test_session.refresh(rec_db)
# }}}

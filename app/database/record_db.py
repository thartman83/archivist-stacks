###############################################################################
# record_db.py for Archivist Stacks database models                           #
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
"""Record database models."""
# }}}

# record_db {{{
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import mapped_column, Session
from app.models import Record, RecordCreate
from app.database import Base


class RecordDB(Base):  # pylint: disable=too-few-public-methods
    """SQL Alchemy record model."""

    __tablename__ = "record"

    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String, index=True)
    filename = mapped_column(String, index=True)
    record_path = mapped_column(String)
    checksum = mapped_column(String)
    size = mapped_column(Integer)
    created = mapped_column(DateTime)
    mimetype = mapped_column(String)


# Crud utilities
def create_record(record: RecordCreate, db: Session) -> Record:
    """Create a record."""
    try:
        db_record = RecordDB(**record.model_dump())
        db.add(db_record)

        db.commit()
        db.refresh(db_record)
        return Record(**db_record.__dict__)
    except SQLAlchemyError as ex:
        db.rollback()
        raise ex


def get_record_by_id(record_id: int, db: Session) -> Record:
    """Return a record by id."""
    return db.query(RecordDB).filter(RecordDB.id == record_id).first()
# }}}

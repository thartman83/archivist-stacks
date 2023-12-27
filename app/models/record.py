###############################################################################
#  record.py for Archivist Stacks models                                     #
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
"""Record model."""
# }}}

#  {{{
from datetime import datetime
from pydantic import BaseModel, Field, FilePath, ValidationError
from sqlalchemy import Column, Integer, String, DateTime, exc
from app.common import DB_Base, Session


class RecordBase(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic Record base model."""

    title: str
    filename: str
    record_path: FilePath
    checksum: str
    size: int
    mimetype: str
    created: datetime = Field(default=datetime.now())
    modified: datetime = Field(default=datetime.now())


class RecordCreate(RecordBase):  # pylint: disable=too-few-public-methods
    """Pydantic Record model for creating records."""

    pass  # pylint: disable=unnecessary-pass


class Record(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic Record model."""

    id: int

    class Config:  # pylint: disable=too-few-public-methods
        """ORM support for model."""

        orm_mode: True


class RecordDB(DB_Base):  # pylint: disable=too-few-public-methods
    """SQL Alchemy record model."""

    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    filename = Column(String, index=True)
    record_path = Column(String)
    checksum = Column(String)
    size = Column(Integer)
    created = Column(DateTime)
    modified = Column(DateTime)
    mimetype = Column(String)


# Crud utilities
def create_record(record: Record) -> Record:
    """Create a record."""
    try:
        db_record = RecordDB(**record.dict())
        Session.add(db_record)

        Session.commit()
        Session.refresh(db_record)

        record.id = db_record.id
    except ValidationError as ex:
        raise ex
    except exc.SQLAlchemyError as ex:
        Session.rollback()
        raise ex


def get_record_by_id(record_id: int):
    """Return a record by id."""
    return Session.query(RecordDB).filter(RecordDB.id == record_id).first()


# }}}

###############################################################################
#  collection_db.py for Archivist Stacks database models                      #
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
"""Collection Database model."""
# }}}

# collection_db {{{
from typing import List
from sqlalchemy import Integer, ForeignKey, Table, Column, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy.orm import relationship
from app.database import Base, EditionDB, RecordDB
from app.models import RecordCreate, CollectionCreate
from app.models import Collection

assoc_table = Table(
    "collection_x_edition",
    Base.metadata,
    Column("collection_id", ForeignKey("collection.id"), primary_key=True),
    Column("edition_id", ForeignKey("edition.id"), primary_key=True)
)


class CollectionDB(Base):  # pylint: disable=too-few-public-methods
    """SQL Alchemy collection model."""

    __tablename__ = "collection"

    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String, index=True)
    current_edition_id: Mapped[int] = mapped_column(ForeignKey("edition.id"))
    current_edition: Mapped[EditionDB] = relationship(lazy='joined')
    editions: Mapped[List[EditionDB]] = relationship(secondary=assoc_table,
                                                     lazy='joined')


def create_collection(collection: CollectionCreate, record: RecordCreate,
                      db: Session) -> Collection:
    """Create a new collection."""
    try:

        rec_db = RecordDB(**record.model_dump())

        ed_db = EditionDB(native=rec_db)

        collection_db = CollectionDB(**collection.model_dump(),
                                     current_edition=ed_db, editions=[ed_db])
        db.add(collection_db)
        db.commit()
        db.refresh(collection_db)

        return Collection(**collection_db.__dict__)
    except SQLAlchemyError as ex:
        db.rollback()
        raise ex


def add_edition(collection: Collection, record: RecordCreate,
                db: Session) -> Collection:
    """Add an edition to a collection."""
    try:
        rec_db = RecordDB(**record.model_dump())
        ed_db = EditionDB(native=rec_db)

        col_db: CollectionDB = db.query(CollectionDB).filter(
            CollectionDB.id == collection.id).first()
        col_db.current_edition = ed_db
        col_db.editions.append(ed_db)

        db.commit()
        db.refresh(col_db)
        return Collection(**col_db.__dict__)
    except SQLAlchemyError as ex:
        db.rollback()
        raise ex


def find_collection_by_id(col_id: int, db: Session) -> Collection:
    """Find a collection by id."""
    try:
        col = db.query(CollectionDB).filter(CollectionDB.id == col_id).first()
        if col is None:
            return None
        else:
            return Collection(**col.__dict__)
    except SQLAlchemyError as ex:
        raise ex

# }}}

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
from sqlalchemy import UniqueConstraint
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy.orm import relationship
from app.database import Base, EditionDB, RecordDB
from app.models import RecordCreate, CollectionCreate
from app.models import Collection, Edition


col_x_ed = Table(
    "collection_edition_assoc",
    Base.metadata,
    Column("collection_id", ForeignKey("collection.id"), primary_key=True,
           index=True),
    Column("edition_id", ForeignKey("edition.id"), primary_key=True,
           index=True),
    UniqueConstraint("collection_id", "edition_id"))


class CollectionDB(Base):  # pylint: disable=too-few-public-methods
    """SQL Alchemy collection model."""

    __tablename__ = "collection"

    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String, index=True)
    current_edition_id: Mapped[int] = mapped_column(ForeignKey("edition.id"))
    current_edition: Mapped[EditionDB] = relationship(lazy='joined')
    editions: Mapped[List[EditionDB]] = relationship(secondary=col_x_ed,
                                                     lazy='joined')


def create_collection(collection: CollectionCreate, record: RecordCreate,
                      db: Session) -> Collection:
    """Create a new collection."""
    try:

        rec_db = RecordDB(**record.model_dump())

        ed_db = EditionDB(native=rec_db, edition_number=0)

        collection_db = CollectionDB(**collection.model_dump(),
                                     current_edition=ed_db, editions=[ed_db])
        db.add(collection_db)
        db.commit()
        db.refresh(collection_db)

        return Collection(**collection_db.__dict__)
    except SQLAlchemyError as ex:
        db.rollback()
        raise ex


def add_edition(collection_id: int, record: RecordCreate,
                db: Session) -> Collection:
    """Add an edition to a collection."""
    try:
        collection = db.query(CollectionDB).filter(CollectionDB.id ==
                                                   collection_id).first()

        rec_db = RecordDB(**record.model_dump())
        max_edition = max(collection.editions,
                          key=lambda x: x.edition_number)
        ed_db = EditionDB(native=rec_db,
                          edition_number=max_edition.edition_number+1)

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

        return Collection(**col.__dict__)
    except SQLAlchemyError as ex:
        raise ex


def find_edition_by_edition_number(col_id: int, ed_number: int,
                                   db: Session) -> Edition:
    """Find an edition by the collection id and the edition number."""
    try:
        ed = db.query(EditionDB).join(col_x_ed).filter(
            (col_x_ed.c.collection_id == col_id) &
            (EditionDB.edition_number == ed_number)).first()

        if ed is None:
            return None

        return Edition(**ed.__dict__)
    except SQLAlchemyError as ex:
        raise ex

# }}}

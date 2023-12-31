###############################################################################
#  edition_db.py for Archivist Stacks database models                         #
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
"""Edition ORM representation."""
# }}}

# edition_db {{{
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy.orm import relationship
from app.database import Base, RecordDB
from app.models import Edition, EditionCreate


class EditionDB(Base):  # pylint: disable=too-few-public-methods
    """SQL Alchemy edition model."""

    __tablename__ = "edition"

    id = mapped_column(Integer, primary_key=True, index=True)
    edition_number = mapped_column(Integer, index=True, nullable=False)
    native_id: Mapped[int] = mapped_column(ForeignKey("record.id"))
    native: Mapped["RecordDB"] = relationship(lazy='joined')

    #  edition_number = relationship('collection_edition_assoc',
    #  back_populates='edition_number')


def create_edition(ed: EditionCreate, db: Session) -> Edition:
    """Add a new edition."""
    try:
        db_ed = EditionDB(native_id=ed.native.id,
                          page_count=ed.page_count)
        db.add(db_ed)
        db.commit()
        db.refresh(db_ed)
        return Edition(**db_ed.__dict__)
    except SQLAlchemyError as ex:
        db.rollback()
        raise ex


def get_edition_by_id(edition_id: int, db: Session) -> Edition:
    """Return an edition by id."""
    ed = db.query(EditionDB).filter(EditionDB.id == edition_id).first()
    return Edition(**ed.__dict__)


# }}}

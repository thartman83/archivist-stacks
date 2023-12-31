###############################################################################
#  collection_router.py for Archivist Stacks routers modules                  #
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
"""Collection routes."""
# }}}

# collection_router {{{
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database import (
    get_db, find_collection_by_id, create_collection,
    add_edition, find_edition_by_edition_number
)
from app.models import RecordCreate, CollectionCreate
from app.models import Collection, Edition
from app.common import Storage, Config

CollectionRouter = APIRouter(prefix='/collection', tags=['collection'])
storage = Storage(Config())


@CollectionRouter.get('/{collection_id}', response_model=Collection)
async def get_collection(collection_id: int, db: Session = Depends(get_db)):
    """Return a collection."""
    collection = find_collection_by_id(collection_id, db)
    if collection is None:
        raise HTTPException(404, f"Collection {collection_id} not found.")

    return collection


@CollectionRouter.get('/{collection_id}/editions/{edition_id}')
async def get_edition(collection_id: int, edition_number,
                      db: Session = Depends(get_db)):
    """Return an edition from a collection."""
    ed: Edition = find_edition_by_edition_number(collection_id,
                                                 edition_number, db)
    if ed is None:
        raise HTTPException(404, f"""Edition {edition_number} not found in
        collection {collection_id}""")

    return ed


@CollectionRouter.post('', response_model=Collection,
                       status_code=status.HTTP_201_CREATED)
async def add_collection(title: str, upload: UploadFile,
                         db: Session = Depends(get_db)):
    """Create a new collection."""
    try:
        record_path, checksum, size = storage.store_record(upload)
        rec_create = RecordCreate(title=title,
                                  filename=upload.filename,
                                  record_path=record_path,
                                  checksum=checksum,
                                  size=size,
                                  mimetype=upload.content_type)

        col_create = CollectionCreate(title=title)

        collection = create_collection(col_create, rec_create, db)
    except SQLAlchemyError as ex:
        storage.rollback_record(record_path)
        raise ex

    return collection


@CollectionRouter.post('/{collection_id}/editions',
                       status_code=status.HTTP_201_CREATED)
async def add_new_edition(collection_id, title: str, upload: UploadFile,
                      db: Session = Depends(get_db)):
    """Add a new edition to an existing collection."""
    try:
        record_path, checksum, size = storage.store_record(upload)
        rec_create = RecordCreate(title=title,
                                  filename=upload.filename,
                                  record_path=record_path,
                                  checksum=checksum,
                                  size=size,
                                  mimetype=upload.content_type)
        collection = add_edition(collection_id, rec_create, db)
    except SQLAlchemyError as ex:
        storage.rollback_record(record_path)
        raise ex

    return collection
# }}}

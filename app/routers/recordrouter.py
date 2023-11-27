###############################################################################
#  recordReouter.py for archivist stacks                                      #
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
"""Record routes."""
# }}}

# recordReouter {{{
import shutil
from typing import Dict
from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import ValidationError
from starlette import status
from app.common import Storage, Config
from ..models import Record
RecordRouter = APIRouter(prefix='/records', tags=['record'])

records: Dict[int, Record] = {}
storage = Storage(Config())


@RecordRouter.get('/{record_id}')
async def get_record(record_id: int):
    """Return a record by id."""
    if record_id not in records:
        raise HTTPException(
            status_code=404, detail=f"Unknown record {record_id}")

    return records[record_id]


@RecordRouter.post('', status_code=status.HTTP_201_CREATED)
async def add_record(upload: UploadFile, name: str):
    """Add a record."""
    try:

        record_path, checksum, recordid = storage.store_record_file(upload)
        record = Record(id=recordid, name=name,
                        filename=upload.filename,
                        record_path=record_path,
                        checksum=checksum)
        records[record.id] = record
    except shutil.Error as err:
        detail = f"Internal server error: {str(err)}"
        raise HTTPException(status_code=500,
                            detail=detail) from err
    except FileNotFoundError as err:
        detail = f"Internal Server error: {str(err)}"
        raise HTTPException(status_code=500,
                            detail=detail) from err
    except ValidationError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    return record


@RecordRouter.delete('/{record_id}')
async def delete_record(record_id: int):
    """Delete record."""
    if record_id not in records:
        raise HTTPException(status_code=404,
                            detail=f"Unknown record {record_id}")

    records.pop(record_id)
    return {
        "details": f"Record {record_id} deleted"
    }
# }}}

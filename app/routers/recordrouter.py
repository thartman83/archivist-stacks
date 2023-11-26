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
from typing import Dict
from fastapi import APIRouter, HTTPException, UploadFile
from starlette import status
from ..models import Record
RecordRouter = APIRouter(prefix='/records', tags=['record'])

records: Dict[int, Record] = {}


@RecordRouter.get('/{record_id}')
async def get_record(record_id: int):
    """Return a record by id."""
    if record_id not in records:
        raise HTTPException(
            status_code=404, detail=f"Unknown record {record_id}")

    return records[record_id]


@RecordRouter.post('', status_code=status.HTTP_201_CREATED)
async def add_record(upload: UploadFile):
    """Add a record."""
    nextid = get_nextid()
    record = Record(id=nextid, name=upload.filename)
    record.id = nextid
    records[nextid] = record

    return record


def get_nextid():
    """Return the next available recordid."""
    return 1 if len(records) == 0 else max(records.keys()) + 1


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

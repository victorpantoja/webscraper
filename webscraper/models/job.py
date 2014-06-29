# coding: utf-8
from bson.objectid import ObjectId
from datetime import datetime
from scraper.repository import Repository, Property, Collection


STATUS_CREATED = "created"
STATUS_EXECUTING = "executing"
STATUS_FINISHED = "finished"


class Job(Collection, Repository):
    __collection__ = 'job'

    _id = Property(ObjectId, "job id")
    global_id = Property(unicode, "global id")
    status = Property(unicode, "job status")
    started_at = Property(datetime, "updated time")
    completed_at = Property(datetime, "updated time")

""" BaseModel class for holding database data """
import logging
import datetime
from paktrack.common.common import (get_axis_data)
from bson import ObjectId
from pymongo import MongoClient


def get_mongo_connection_string(db_user, db_pass, db_host, db_port, db):
    conn_string = "mongodb://"
    if db_user and db_pass:
        conn_string = conn_string  + db_user + ":" + db_pass + "@"
    conn_string = conn_string + db_host + ":" + str(db_port) + "/" + db
    return conn_string


class BaseModel(object):
    """A Baseclass for all database object"""
    def __init__(self, db_host, db_port, db, db_user, db_pass, collection_name):
        connection_string = get_mongo_connection_string(db_user, db_pass, db_host, db_port, db)
        self.db_client = MongoClient(connection_string)
        self.db = self.db_client[db]
        self.collection = self.db[collection_name]
        # create logger
        self.logger = logging.getLogger(__name__)


    def get_events(self, truck_id, package_id, is_above_threshold=True):

        self.logger.info("Started loading events from mongodb cursor")

        events = []
        query = {"truck_id": truck_id, "package_id": package_id, "is_above_threshold": is_above_threshold, "is_processed": {"$exists":True}, "x": {"$exists": True}, "y": {"$exists":True}, "z": {"$exists": True}}
        cursor = self.get_cursor(query)

        for line in cursor:
            events.append(get_axis_data(line))

        if not cursor:
            query = {"truck_id":truck_id,"package_id":package_id, "is_above_threshold": is_above_threshold, "is_processed": {"$exists":True}, "value.x":{"$exists":True}, "value.y": {"$exists":True}, "value.z": {"$exists":True}}
            cursor = self.get_cursor(query)

        for line in cursor:
            events.append(get_axis_data(line))

        self.logger.info("Done loading events from mongodb cursor")

        return events

    def get_event(self, id):
        query = {"_id":ObjectId(id),"value.x":{"$exists":True},"value.y":{"$exists":True},"value.z":{"$exists":True}}
        event = self.collection.find_one(query)

        if event:
            event = get_axis_data(event)
        else:
            query = {"_id": ObjectId(id), "x": {"$exists": True}, "y": {"$exists": True}, "z": {"$exists": True}}
            event = self.collection.find_one(query)
            event = get_axis_data(event)

        return event

    def get_cursor(self, query, fields={"dummy": 0}):
        cursor = self.collection.find(query, fields)
        return cursor

    def update(self, event):
        self.logger.info(
            "Started udpating database for %s event of id: %s",
            self.collection.name, event['_id'])
        event['updated_at'] = datetime.datetime.utcnow().strftime(
            '%Y-%m-%d %H:%M:%S')

        self.collection.save(event)

        self.logger.info(
            "Done udpating database for %s event of id: %s",
            self.collection.name, event['_id'])

    def delete(self, event):
        self.collection.remove({"_id": event['_id']})
        self.logger.info(
            "Done deleting %s of id: %s", self.collection.name, event['_id'])

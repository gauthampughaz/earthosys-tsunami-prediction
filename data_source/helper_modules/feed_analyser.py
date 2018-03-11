from quakefeeds import QuakeFeed
from data_processor import process_data
from datetime import datetime
import os
import sys
import sqlite3
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../earthosys_model/model")
from tsunami_predictor import predict_tsunami

db_file = os.path.dirname(os.path.abspath(__file__)) + "/../../earthosys_site/db.sqlite3"


def get_feeds():
    id_buffer, feeds_id = set(), set()
    while True:
        feeds = QuakeFeed("2.5", "day")
        id_buffer = get_ids(feeds) & id_buffer
        for feed in range(len(feeds)):
            if feeds[feed]["id"] not in id_buffer:
                data = []
                id_buffer.add(feeds[feed]["id"])
                magnitude = feeds.magnitude(feed)
                if magnitude >= 4.0:
                    data.append(magnitude)
                    data.append(feeds.depth(feed))
                    data += feeds.location(feed)[::-1]
                    tsunami, region = predict(data)
                    try:
                        log_data(data, region, tsunami)
                    except Exception as e:
                        print(e)


def get_ids(feeds):
    ids = set()
    for feed in feeds:
        ids.add(feed["id"])
    return ids


def predict(data):
    _input = process_data(input_data=data)
    return predict_tsunami([_input]), _input[2]


def log_data(data, region, tsunami):
    print(data, region, tsunami)
    sql = ''' INSERT INTO feeds_feedprediction(magnitude, depth, latitude, longitude, epicenter, date_time, tsunami) VALUES(?, ?, ?, ?, ?, ?, ?) '''
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(sql, data + [region, datetime.now(), tsunami])
    connection.commit()
    cursor.close()
    connection.close()


def create_connection():
    global db_file
    try:
        connection = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        connection = None
    return connection

if __name__ == "__main__":
    get_feeds()

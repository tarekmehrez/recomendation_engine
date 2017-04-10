# Abdelrahman
import re
import csv
import os
import sys
import pymysql
import argparse
import logging

# DATABASE INITIALIZATION

# db = pymysql.connect(host="azure.3bont.com",  # your host, usually localhost
#                      # your username
#                      user="ameniawy",
#                      # your password
#                      passwd="@3Bont.com",
#                      db="tresbon")  # name of the data base
# db.set_charset('utf8mb4')


db = pymysql.connect(host="localhost",  # your host, usually localhost
                     # your username
                     user="root",
                     # your password
                     passwd="root",
                     db="threebont")  # name of the data base
db.set_charset('utf8mb4')
# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()


def save_data(lang, data):
    """
        Saves data from DB query into .txt files.

        Args:
                lang(str): lang of articles fetched.
                data(list): list of articles
                list of entries
                entry = [0 category, 1 post_date, 2 title, 3 summary, 4 content, 5 id]

    """
    #index = 1
    for entry in data:

        date = str(entry[1])[:10]
        category = entry[0]
        title = entry[2]
        summary = entry[3]
        body = entry[4]
        _id = entry[5]
        name = str(category) + '_' + str(_id)
        filename = "data_try/%s/%s/%s.txt" % (lang, date, name)
        #index += 1

        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise



        with open(filename, "w") as f:
            if str(category) == 'twitter':
                f.write(str(summary))
            else:
                f.write(str(title))
                f.write(str(body))
            f.close()

parser = argparse.ArgumentParser()
parser.add_argument("start_date", help="add starting date for query")
parser.add_argument("end_date", help="add ending date for query")
args = parser.parse_args()

# mysql query
# en call
logging.info('Starting DB call for EN articles..this might take a while..')
cur.execute(
    'SELECT  `category`, `post_date`, `title`, `summary`, `content`, `id`  FROM `content` WHERE `post_date` >= %s AND `post_date` <= %s AND  `lang` = %s AND ( `category` = "articles" OR `category` = "facebook" OR `category` = "twitter")', (args.start_date, args.end_date, "en"))
data = cur.fetchall()
save_data("en", data)

# ar call
logging.info('Starting DB call for AR articles..this might take a while..')
cur.execute(
    'SELECT  `category`, `post_date`, `title`, `summary`, `content`, `id`  FROM `content` WHERE `post_date` >= %s AND `post_date` <= %s AND  `lang` = %s AND ( `category` = "articles" OR `category` = "facebook" OR `category` = "twitter")', (args.start_date, args.end_date, "ar"))
data = cur.fetchall()
save_data("ar", data)




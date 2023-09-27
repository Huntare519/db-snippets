from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import argparse
from datetime import datetime

import os

load_dotenv()


def get_db_client():
    db_password = os.environ.get('DB_PASSWORD')
    uri = f"mongodb+srv://hfgoff:{db_password}@cluster0.kz8zjef.mongodb.net/?retryWrites=true&w=majority"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client


def ping_db(client):
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        exit(1)


def get_year():
    while True:
        year = input(
            "Enter the year you read this book [2020, 2021, 2022, 2023, enter for 2012]: ")
        if len(year) == 4 and year.isdigit():
            return year
        print("Invalid input. Please enter a 4-digit year.")


def update_books(collection):
    for book in collection.find():
        print("Title:", book.get("title"), "Author:", book.get("author"))
        year = get_year()
        dt_object = datetime.strptime(year, "%Y")
        unix_ts = int(dt_object.timestamp())

        collection.update_one({"_id": book.get("_id")}, {
                              "$set": {"yearRead": unix_ts}})
        print("Updated book with title:", book.get(
            "title"), "You read it in", year)


def main():
    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('--test', type=bool, nargs="?",
                        help='which database to use')
    args = parser.parse_args()
    if args.test is None:
        test = "test"  # default to test database
    else:
        test = args.test

    client = get_db_client()
    ping_db(client)

    db = client[test]
    collection = db["books"]
    update_books(collection)


if __name__ == "__main__":
    main()

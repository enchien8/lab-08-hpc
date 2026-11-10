#!/usr/bin/env python3
"""Print paths for books that do not yet have an LLM analysis in MongoDB."""

import logging
import os
import sys

from pymongo import MongoClient
from pymongo.errors import PyMongoError

logger = logging.getLogger(__name__)


def pending_books(books):
    """Return the file keys of documents without an llm_analysis field."""
    cursor = books.find(
        {"llm_analysis": {"$exists": False}},
        {"_id": 1},
    ).sort("_id", 1)
    return [document["_id"] for document in cursor]


def main():
    """Print the header and paths of pending books in the supplied directory."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    if len(sys.argv) != 2:
        logger.error("Usage: pending.py BOOK_DIR")
        sys.exit(1)

    book_dir = sys.argv[1]
    client = MongoClient(
        os.environ["MONGODB_ATLAS_URL"],
        username=os.environ["MONGODB_ATLAS_USER"],
        password=os.environ["MONGODB_ATLAS_PWD"],
    )
    try:
        books = client["gutenberg"]["books"]
        keys = pending_books(books)
        print("File path")
        for key in keys:
            print(os.path.join(book_dir, key))
    except PyMongoError as e:
        logger.error("Cannot query MongoDB: %s", e)
        raise
    finally:
        client.close()


if __name__ == "__main__":
    main()

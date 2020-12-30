
import sqlite3
import os
import sys

from itertools import chain

from . import argparser
from .adapters import register
from .database import (
    execute_schema,
    check_schema,
    insert_food,
    insert_mood
)


def main(*argv):

    args = argparser().parse_args(argv if argv else None)

    foodlist = []
    mood = None

    if args.foodlist:
        foodlist = [tuple(f.split(':')) for f in chain(*args.foodlist)]
        if (failed := list(filter(lambda f: len(f) != 2 or not all(f), foodlist))):
            raise Exception(f'Incorrect food data format: {list(failed)}')
    else:
        mood = args.moodstatus.split(':')
        if not all(mood) or len(mood) != 2:
            raise Exception(f'Incorrect mood data format: {args.moodstatus}')

    initdb = False
    if os.access(args.dbfilepath, mode=os.F_OK):
        if not os.access(args.dbfilepath, mode=os.W_OK):
            raise EnvironmentError(
                f'fml: Unable to operate on databse "{args.dbfilepath}"')
    else:
        # If file does not exist, we need to create it and initialize
        initdb = True

    if initdb:
        with open(args.dbfilepath, 'bw+') as fp:
            # If we are initializing, we must be sure file is empty
            fp.truncate()
            initdb = True

    # Open file and read the database
    db = sqlite3.connect(args.dbfilepath)

    # Register type adapters for python types
    register()

    # Create necessary tables
    if initdb or not check_schema(db):
        execute_schema(db)

    if foodlist:
        for f in foodlist:
            insert_food(db, *f)
    else:
        insert_mood(db, *mood)

    db.commit()
    db.close()


# Yes
if __name__ == '__main__':
    main(*sys.argv)

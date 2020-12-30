"""Food mood logger library."""

import argparse

from datetime import datetime
from importlib import resources

__version__ = resources.read_text('fml', 'VERSION')

__all__ = ['argparser', 'main']


def argparser():
    parser = argparse.ArgumentParser('fml',
                                     description="""
    fml (Food-Mood Logger) is a food-mood relation manual logging tool used
    to find corelation of consumed food and mood drops. First you set the
    food you ate, it will be put into the database with mood references set
    to NULL. Then you set the mood you were in after said consumption, and
    the database trigger fills missing references with mood row IDs.
    """)
    parser.add_argument(
        '-d', '--database',
        dest='dbfilepath',
        metavar='food-mood-log.db',
        type=str,
        action='store',
        default='food-mood-log.db',
        help='Database file path.')
    parser.add_argument(
        '-t', '--timestamp',
        dest='timestamp',
        metavar=datetime.now(),
        type=datetime,
        action='store',
        default=datetime.now(),
        help='Log message date (either mood or consumption timestamp). If not\
        set, current time will be used.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-f', '--food',
        dest='foodlist',
        metavar='sugar:50',
        nargs='+',
        type=str,
        action='append',
        help='Food and grammes of thereof.')
    group.add_argument(
        '-m', '--mood',
        dest='moodstatus',
        metavar='doom:100',
        type=str,
        action='store',
        help='Mood and its score in scale 1-100.')

    return parser

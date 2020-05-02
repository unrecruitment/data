import glob
import csv
from zipfile import ZipFile
import datetime
import contextlib

import logging
log = logging.getLogger("linkedin.archives")

import pandas as pd
pd.set_option('display.max_colwidth', -1)

class Data:
    def __init__(self, path):
        userglob = f'{path}/*'
        log.debug(f"Looking for users at {userglob!r}...")
        self.people = [Person(p) for p in glob.glob(userglob)]
        if not self.people:
            raise FileNotFoundError("No users found.")


class Person:
    def __init__(self, path):
        self.path = path
        self.name = path.split('/')[-1]
        self.archives = []
        for p in sorted(glob.glob(f'{path}/*.zip'), key=self._extract_archive_date):
            self.archives.append(Archive(p))
            with contextlib.suppress(AttributeError):
                print(len(self.archives[-1].posts))

    @staticmethod
    def _extract_archive_date(path):
        return datetime.datetime.strptime(path.split('_')[-1], '%m-%d-%Y.zip')

    @property
    def posts(self):
        for a in self.archives:
            with contextlib.suppress(AttributeError):
                posts = a.posts
        return posts


class Archive:
    def __init__(self, path):
        with ZipFile(path) as zipfile:
            log.debug(f"Processing: {path}")
            with contextlib.suppress(KeyError):
                with zipfile.open('Shares.csv') as stream:
                    self.posts = pd.read_csv(stream, parse_dates=[])
                    self.posts.set_index(self.posts.pop('Date'), inplace=True)
                    self.posts['ShareCommentary'] = self.posts['ShareCommentary'].str.replace('"\r\n"', '\n')

#!/usr/bin/env python3

import os
import sys
import math

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

import ruamel.yaml
yaml = ruamel.yaml.YAML()

from linkedin.archives import Data, Archive
import numpy as np


for person in Data('users').people:
    if len(sys.argv) > 1:
        posts = Archive(sys.argv[1]).posts
    else:
        posts = person.posts

    posts = posts[~posts.index.duplicated()]
    data = posts.to_dict(orient='index')
    for record in data.values():
        for key, value in list(record.items()):
            if isinstance(value, float) and math.isnan(value):
                del record[key]
    yaml_path = f'{person.path}/posts.yaml'
    log.debug(f"Writing to {yaml_path!r}...")
    with open(yaml_path, 'w') as stream:
        yaml.dump({'posts': data}, stream)

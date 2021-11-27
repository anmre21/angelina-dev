"""Markdown testing.

Markdown metadata should be formatted like:
title: my dogs
published: 2021-11-27
description: Pics of my dogs!
"""
from pathlib import Path
from itertools import islice
import datetime
import os

# print(str(Path('angelina-dev/')))
# while str(Path.cwd().parents) != 'angelina-dev':
#     print(str(Path.cwd()))
#     os.chdir('..')
#     break
src = Path('./src')
assert src.exists()

for file in src.iterdir():
    if file.is_file():
        with file.open("r") as f:
            lines = list(islice(f, 3))

    # Check all metadata tags are present
    metadata = [line.split()[0] for line in lines]
    assert metadata == ['title:', 'published:', 'description:']

    # Check date is valid
    date_str = lines[1].split()[1]
    assert datetime.datetime.strptime(date_str, '%Y-%m-%d')

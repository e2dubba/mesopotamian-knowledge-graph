#!/usr/bin/env python4
"""A script for managing posts, both converting jupyter notebooks and creating
new posts"""

import datetime
from collections import namedtuple
import subprocess
import os
import re


HEADER = namedtuple("Header", "layout title author category tags")
EDITOR = os.environ.get("EDITOR", "vim")


def write_header(header):
    """Function for formating the header string for use in the post files"""
    string = """---
title: {}
layout: {}
author: {}
tags: {}
category: {}
---
"""
    string = string.format(
        header.title,
        header.layout,
        header.author,
        ", ".join(header.tags),
        header.category,
    )
    print(string)
    return string


def main():
    aparser = argparse.ArgumentParser()
    aparser.add_argument(
        "-u",
        "--update",
        help="Updates an already existing file, and not a new dated item",
        action="store_true",
    )
    aparser.add_argument(
        "-i",
        "--ipynb",
        help="Convert a Jupyter notebook to markdown, notebooks should be camel cased",
    )
    aparser.add_argument("-c", "--category", help="Specify the category of the post")
    aparser.add_argument(
        "-t",
        "--tags",
        help="Specify tags for the post, make them comma seperated.\
                Like: `python,machinelearning`",
    )

    aparser.add_argument("title", nargs="?", help="Create a new markdown file")

    args = aparser.parse_args()
    if args.ipynb:
        file_name = args.ipynb
        # title = re.sub(r"([A-Z][a-z]+)", r" \1", args.ipynb).strip()
    title = args.title
    if args.tags:
        tags = [tag for tag in args.tags.split(",")]
    else:
        tags = []
    header = HEADER(
        title=title, layout="post", author="", tags=tags, category=args.category
    )

    if not args.update:
        date = datetime.datetime.now()
        date_str = date.strftime("%Y-%m-%d-")
        title = date_str + title

    title = title.replace(" ", "_")
    if args.ipynb:
        # title = os.path.basename(title)
        # title, _ = os.path.splitext(title)
        # out_file = "_posts/{}.md".format(title)
        out_file = "{}.md".format(title)
        subprocess.call(
            [
                "jupyter",
                "nbconvert",
                "--to",
                "markdown",
                "--output",
                out_file,
                "--output-dir=./_posts/",
                file_name,
            ]
        )
        with open("./_posts/{}.md".format(title), "r") as f:
            content = f.read()
        with open("./_posts/{}.md".format(title), "w") as f:
            heading_string = write_header(header)
            f.write(heading_string + content)
    else:
        out_file = "_posts/{}.md".format(title)
        with open(out_file, "w+") as f:
            heading_string = write_header(header)
            f.write(heading_string)
        subprocess.call([EDITOR, out_file])


if __name__ == "__main__":
    import argparse

    main()

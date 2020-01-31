#!/usr/bin/env python3
"""A script for managing posts, both converting jupyter notebooks and creating
new posts.

This funciton requires git and jupyter nbconvert. Both o fthose command line
utilities should be installed before running this command.


This command also defaults to using vim as the editior of choice. It relies on
the system defined Editor in the shell rc.

"""

import datetime
from collections import namedtuple
import subprocess
import os
import shutil


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
        header.title,
    )
    return string


def find_git_username():
    """
    call's git to find the user name.
    """
    call = subprocess.run(
        ["git", "config", "--global", "user.name"], stdout=subprocess.PIPE
    )
    return call.stdout.decode("UTF8").strip()


def draft_writer(header, heading, file_name):
    """
    Create draft file and open in it the text editor
    """
    if not file_name:
        title = heading.replace(" ", "_")
        out_file = os.path.join("drafts/", title + ".md")
    else:
        out_file = os.path.join("drafts", file_name)
    with open(out_file, "w+") as f:
        heading_string = write_header(header)
        heading_string += "\n# {}".format(header.title)
        f.write(heading_string)
    subprocess.call([EDITOR, out_file])


def updater(header, title, file_name):
    """
    Update a a draft to a post in the _posts directory
    """
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d-")
    dest_name = date + os.path.basename(file_name)
    shutil.move(file_name, os.path.join("_posts", dest_name))


def ipynb(header, title, file_name):
    """
    Convert a jupyter notebook into a markdown file, prefixed with the date of
    the script is run
    """
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d-")
    out_file = os.path.splitext(os.path.basename(file_name))[0]
    out_file = date + out_file + ".md"
    out_dir = "./docs/_posts"
    subprocess.call(
        [
            "jupyter",
            "nbconvert",
            "--to",
            "markdown",
            "--output",
            out_file,
            "--output-dir={}".format(out_dir),
            file_name,
        ]
    )
    with open(os.path.join(out_dir, out_file), "r") as filep:
        content = filep.read()
    with open(os.path.join(out_dir, out_file), "w") as filep:
        heading_string = write_header(header)
        filep.write(heading_string + content)


def main():
    parent_parser = argparse.ArgumentParser(
        description="""
    This command line utility is designed to manage posts for a github project
    website. The three options are for creating a draft in the drafts folder,
    updating a draft to a post and moving a Jupyter notebook from the notebooks
    folder to a markdown file to be read by Jekyll.
    """
    )
    subparsers = parent_parser.add_subparsers(
        help="Desired Action to perform", dest="action"
    )

    draft_parser = subparsers.add_parser("draft", help="Create a draft file")
    draft_parser.set_defaults(func=draft_writer)
    update_parser = subparsers.add_parser(
        "update", help="Update a draft and move it to _docs"
    )
    update_parser.set_defaults(func=updater)
    # update_parser.add_argument("file", help="File that needs to be updated")
    ipynb_parser = subparsers.add_parser(
        "ipynb",
        # add_help=False,
        help="Update iPython Notebook to a post",
    )
    # ipynb_parser.add_argument("ipynb_file", help="Notebook to update")
    ipynb_parser.set_defaults(func=ipynb)

    for _, aparser in subparsers.choices.items():
        aparser.add_argument(
            "-c", "--category", help="Specify the category of the post"
        )
        aparser.add_argument(
            "-t",
            "--tags",
            help="Specify tags for the post, make them comma seperated.\
                    Like: `python,machinelearning`",
        )
        aparser.add_argument(
            "-a",
            "--author",
            help="Specify the name of the post, otherwise, git username will be assumed",
        )
        aparser.add_argument("-b", "--blogtitle", help="Title for the Blog post")
        aparser.add_argument("-f", "--filename", help="filename")

    args = parent_parser.parse_args()

    file_name = args.filename
    if args.tags:
        tags = [tag for tag in args.tags.split(",")]
    else:
        tags = []
    if args.author:
        author = args.author
    else:
        author = find_git_username()
    if args.blogtitle:
        heading = args.blogtitle
    else:
        heading = args.filename
    header = HEADER(
        title=heading, layout="post", author=author, tags=tags, category=args.category
    )

    args.func(header, args.blogtitle, file_name)


if __name__ == "__main__":
    import argparse

    main()

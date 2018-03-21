#!/usr/bin/env python3
"""
cmake documentation reader

@author: Aurélien Gâteau <mail@agateau.com>
@license: Apache 2.0
"""
import argparse
import os
import shlex
import subprocess

from collections import namedtuple

__appname__ = "cmakedoc"
__version__ = "1.0.1"
__license__ = "Apache 2.0"

DESCRIPTION = """\
cmakedoc makes it easier to search CMake reference documentation.
"""

SOURCES = ["command", "module", "variable", "property"]

Match = namedtuple("Match", ("source", "topic"))


def error(message):
    print("Error: {}".format(message))


def find_matches(source, term):
    terms = term.lower().split(" ")

    def match(line):
        line = line.lower()
        for term in terms:
            if term not in line:
                return False
        return True

    out, err = subprocess.Popen(["cmake", "--help-%s-list" % source],
                                stdout=subprocess.PIPE).communicate()
    lines = str(out, "utf-8").splitlines()
    return [Match(source, x.strip()) for x in lines if match(x)]


def show_doc(match):
    pager = shlex.split(os.environ.get("PAGER", "less"))
    p1 = subprocess.Popen(["cmake", "--help-%s" % match.source, match.topic],
                          stdout=subprocess.PIPE)
    p2 = subprocess.Popen(pager, stdin=p1.stdout)
    p2.wait()


def show_prompt(has_topic):
    if has_topic:
        message = "Enter topic number or search term"
    else:
        message = "Enter search term"
    message += " (empty input or 'q' to quit): "
    try:
        answer = input(message)
    except KeyboardInterrupt:
        print()
        return ""
    answer = answer.lower()
    if answer == "q":
        return ""
    return answer


def main():
    parser = argparse.ArgumentParser()
    parser.description = DESCRIPTION
    parser.add_argument("term", nargs="*", help="Search term")
    args = parser.parse_args()

    if args.term:
        term = " ".join(args.term)
    else:
        term = show_prompt(has_topic=False)
        if term is "":
            return

    while True:
        matches = []
        for source in SOURCES:
            matches.extend(find_matches(source, term))

        if matches:
            print()
            print("# Matching topics:")
            for idx, match in enumerate(matches):
                print("%2d: %s (%s)" % (idx + 1, match.topic, match.source))
        else:
            error("no topics found.")
        print()

        answer = show_prompt(has_topic=len(matches) > 0)

        if answer.isdigit():
            index = int(answer) - 1
            if index < 0 or index >= len(matches):
                error("invalid topic number.")
                continue
            show_doc(matches[index])
        elif answer == "":
            return
        else:
            term = answer


if __name__ == "__main__":
    main()

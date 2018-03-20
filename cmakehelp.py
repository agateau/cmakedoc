#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
cmake documentation reader

@author: Aurélien Gâteau <aurelien.gateau@free.fr>
@license: GPLv3
"""
import sys
import subprocess

from collections import namedtuple

__appname__ = "cmakehelp"
__version__ = "1.0.0"
__license__ = "GPLv3"

DESCRIPTION = """\
cmakehelp makes it easier to search CMake reference documentation. Just enter
any term to get a list of the matching command, module, variable or property.
You can then select the topic you want and read it.
"""

SOURCES = ["command", "module", "variable", "property"]

Match = namedtuple("Match", ("source", "topic"))


def error(message):
    print("Error: {}".format(message))


def find_matches(source, term):
    out, err = subprocess.Popen(["cmake", "--help-%s-list" % source],
                                stdout=subprocess.PIPE).communicate()
    lines = str(out, "utf-8").splitlines()
    return [Match(source, x.strip()) for x in lines if term in x.lower()]


def show_doc(match):
    p1 = subprocess.Popen(["cmake", "--help-%s" % match.source, match.topic],
                          stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["less"], stdin=p1.stdout)
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
    if len(sys.argv) > 1:
        term = sys.argv[1]
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
            error("No match found.")
        print()

        answer = show_prompt(has_topic=len(matches) > 0)

        if answer.isdigit():
            index = int(answer) - 1
            if index < 0 or index >= len(matches):
                error("Wrong topic number")
                continue
            show_doc(matches[index])
        elif answer == "":
            return
        else:
            term = answer


if __name__ == "__main__":
    main()

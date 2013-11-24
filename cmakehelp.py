#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
cmake documentation reader

@author: Aurélien Gâteau <aurelien.gateau@free.fr>
@license: GPLv3
"""
import sys
import subprocess
import tui

SOURCES = ["command", "module", "variable", "property"]

def findMatches(source, term):
    out, err = subprocess.Popen(["cmake", "--help-%s-list" % source], stdout=subprocess.PIPE).communicate()
    term = term.lower()
    return [line.strip() for line in out.splitlines() if term in line.lower()]


def showDoc(source, keyword):
    p1 = subprocess.Popen(["cmake", "--help-%s" % source, keyword], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["less"], stdin=p1.stdout)
    p2.wait()


def showPrompt(hasTopic):
    if hasTopic:
        prompt = "Enter topic number or search term"
    else:
        prompt = "Enter search term"
    prompt += " (empty input or 'q' to quit): "
    try:
        answer = tui.editLine("", prompt)
    except KeyboardInterrupt:
        print
        return None
    answer = answer.lower()
    if answer == "q":
        return ""
    return answer
    

def main():
    if len(sys.argv) > 1:
        term = sys.argv[1]
    else:
        term = showPrompt(hasTopic=False)
        if term is "":
            return

    while True:
        questions = []
        matches = []
        index = 1
        for source in SOURCES:
            lst = findMatches(source, term)
            for keyword in lst:
                matches.append((source, keyword))
                questions.append((index, "%s (%s)" % (keyword, source)))
                index += 1

        if len(matches) > 0:
            print
            print "# Matching topics:"
            for pos, txt in questions:
                print "%2d: %s" % (pos, txt)
        else:
            tui.error("No match found")
        print

        answer = showPrompt(hasTopic=len(matches) > 0)

        if answer.isdigit():
            index = int(answer) - 1
            if index < 0 or index >= len(matches):
                tui.error("Wrong topic number")
                continue
            source, keyword = matches[index]
            showDoc(source, keyword)
        elif answer == "":
            return
        else:
            term = answer

if __name__ == "__main__":
    main()

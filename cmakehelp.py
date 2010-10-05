#!/usr/bin/env python
import sys
import subprocess
import tui

SOURCES = ["command", "module", "variable"]

def findMatches(source, term):
    out, err = subprocess.Popen(["cmake", "--help-%s-list" % source], stdout=subprocess.PIPE).communicate()
    return [line.strip() for line in out.splitlines() if term in line.lower()]


def showDoc(source, term):
    p1 = subprocess.Popen(["cmake", "--help-%s" % source, term], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["less"], stdin=p1.stdout)
    p2.wait()


def promptSearchTerm(default):
    return tui.editLine(default, "Enter search term: ")

def main():
    if len(sys.argv) > 1:
        term = sys.argv[1]
    else:
        term = promptSearchTerm("")
        if term is None:
            return

    while True:
        questions = []
        matches = []
        index = 1
        for source in SOURCES:
            lst = findMatches(source, term.lower())
            for entry in lst:
                matches.append((source, entry))
                questions.append((index, "%s (%s)" % (entry, source)))
                index += 1
        if len(matches) == 0:
            tui.error("No match found")

        questions.append(("s", "Search"))
        questions.append(("q", "Quit"))

        try:
            answer = tui.selectFromList("Select topic", questions, default=None)
        except KeyboardInterrupt:
            print
            return

        if answer is None or answer == "q":
            return
        elif answer == "s":
            term = promptSearchTerm(term)
            if term is None:
                return
        else:
            index = int(answer) - 1
            match = matches[index]
            showDoc(*match)

if __name__ == "__main__":
    main()

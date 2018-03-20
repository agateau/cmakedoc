# CMakeHelp

## What is it?

CMakeHelp is a command-line tool to read CMake documentation. It lets you
search through CMake commands, modules, variables and properties before
displaying the selected topic with `less`.

## Installation

    ./setup.py install

## "Screenshot"

    user@host: cmakehelp pkg

    # Matching topics:
    1: FindPkgConfig (module)
    2: UsePkgConfig (module)

    Enter topic number or search term (empty input or 'q' to quit): 1

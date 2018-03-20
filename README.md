# What is it?

CMakeHelp is a simple command-line tool to read CMake documentation. It lets
you search through CMake commands, modules and variables before displaying the
selected topic with `less`.

# Installation

1. Make sure `cmake` binary is in your path
2. Optionally symlink `cmakehelp.py` somewhere your path, for example:
    cd /usr/local/bin
    ln -s /path/to/cmakehelp/cmakehelp.py cmakehelp

# "Screenshot"

    user@host: cmakehelp pkg

    # Matching topics:
    1: FindPkgConfig (module)
    2: UsePkgConfig (module)

    Enter topic number or search term (empty input or 'q' to quit): 1

# Author

Aurélien Gâteau <mail@agateau.com>

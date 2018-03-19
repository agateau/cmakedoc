# -*- coding: UTF-8 -*-
"""
Helper functions to build CLI applications

@author: Aurélien Gâteau <aurelien.gateau@free.fr>
@license: GPLv3
"""

import readline
import sys
import locale

import colors as C

# Default user encoding. Used to decode all input strings
# This is the central yokadi definition of encoding - this constant is imported
# from all other modules Beware of circular import definition when add
# dependencies to this module
ENCODING = locale.getpreferredencoding()

_answers = []


class IOStream:
    def __init__(self, original_flow):
        self.__original_flow = original_flow
        if sys.platform == 'win32':
            import pyreadline
            self.__console = pyreadline.GetOutputFile()

    def write(self, text):
        if sys.platform == 'win32':
            self.__console.write_color(text)
        else:
            self.__original_flow.write(text)


stdout = IOStream(sys.stdout)
stderr = IOStream(sys.stderr)


def reinject_input(line):
    """Next call to input() will have line set as default text
    @param line: The default text
    """

    # Set readline.pre_input_hook to feed it with our line
    # (Code copied from yagtd)
    def pre_input_hook():
        readline.insert_text(line.encode(ENCODING))
        readline.redisplay()

        # Unset the hook again
        readline.set_pre_input_hook(None)

    if sys.platform != 'win32':
        readline.set_pre_input_hook(pre_input_hook)


def edit_line(line, prompt="edit> "):
    """Edit a line using readline"""
    if line:
        reinject_input(line)

    if len(_answers) > 0:
        line = _answers.pop(0)
    else:
        try:
            line = input(prompt)
        except EOFError:
            line = ""

    # Remove edited line from history:
    #   oddly, get_history_item is 1-based,
    #   but remove_history_item is 0-based
    if sys.platform != 'win32':
        length = readline.get_current_history_length()
        if length > 0:
            readline.remove_history_item(length - 1)

    return line


def error(message):
    print(C.BOLD + C.RED + "Error: %s" % message + C.RESET, file=stderr)


def warning(message):
    print(C.RED + "Warning: " + C.RESET + message, file=stderr)


def info(message):
    print(C.CYAN + "Info: " + C.RESET + message, file=stderr)


def add_input_answers(*answers):
    """Add answers to tui internal answer buffer. Next call to edit_line() will
    pop the first answer from the buffer instead of prompting the user.
    This is useful for unit-testing."""
    _answers.extend(answers)


def clear_input_answers():
    """Remove all added answers. Useful to avoid making a test depend on a "y"
    added by another test.
    """
    global _answers
    _answers = []

# vi: ts=4 sw=4 et

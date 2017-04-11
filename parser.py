#!/usr/bin/env python3.6

import re
import sys


def check_reg(reg):
    if re.match("^\..*", reg) or re.match("(([^%]|^)([%][%])*)\.+$", reg) or re.match(".*([^%]|^)\.{2}.*", reg):
        # check dots, multiple dots, begin,end,middle
        print("Bad format of fmt file, problem with this regular expression: " + reg, file=sys.stderr)
        exit(4)
    if re.match("^\|.*", reg) or re.match("(([^%]|^)([%][%])*)\|+$", reg) or re.match(".*([^%]|^)\|{2}.*", reg):
        # check pipe, multiple pipe, begin,end,middle
        print("Bad format of fmt file, problem with this regular expression: " + reg, file=sys.stderr)
        exit(4)
    if re.match("(([^%]|^)([%][%])*)!+$", reg) or re.match(".*([^%]|^)!{2}.*", reg) or \
            re.match(".*([^%]|^)!\..*", reg) or re.match(".*([^%]|^)!\|.*", reg) or re.match(".*([^%]|^)!\*.*", reg) \
            or re.match(".*([^%]|^)!\+.*", reg):
        # check the screamer, at the end, multiple in the middle and screamer with . or * or | or +
        print("Bad format of fmt file, problem with this regular expression: " + reg, file=sys.stderr)
        exit(4)
    if re.match(".*(([^%]|^)([%][%])*)\(\).*", reg):
        # check empty parentheses
        print("Bad format of fmt file, problem with this regular expression: " + reg, file=sys.stderr)
        exit(4)
    if re.match("^\+.*", reg) or re.match("^\*.*", reg):
        # check plus and multiple character at start
        print("Bad format of fmt file, problem with this regular expression: " + reg, file=sys.stderr)
        exit(4)
    if re.match(".*(([^%]|^)([%][%])*)\.\*.*", reg) or re.match(".*(([^%]|^)([%][%])*)\.\+.*", reg) or \
            re.match(".*(([^%]|^)([%][%])*)\.\|.*", reg) or re.match(".*(([^%]|^)([%][%])*)\|\..*", reg) or \
            re.match(".*(([^%]|^)([%][%])*)\|\+.*", reg) or re.match(".*(([^%]|^)([%][%])*)\|\*.*", reg):
        # check combinations .*,    .+,     .|,     |.,     |+,     |*
        print("Bad format of fmt file, problem with this regular expression: " + reg, file=sys.stderr)
        exit(4)

    last_char = ""
    new_regex = ""
    negation = ""

    for char in reg:
        # special character % as \ in normal regex
        if char == "%":
            if last_char != "%":
                last_char = char
            else:
                new_regex += "[" + "%" + "]"
                negation = ""
                last_char = ""
        # special character ! as ^ in normal regex
        elif char == "!":
            if last_char != "%":
                negation = "^"
                last_char = char
            else:
                new_regex += negation + "!"
                negation = ""
                last_char = ""
        # special character . as ""(concatenate) in normal regex
        elif char == ".":
            if last_char != "%":
                last_char = char
            else:
                new_regex += negation + "\."
                negation = ""
                last_char = ""
        # special characters do the same in my assignment as in normal regex
        elif char == "|" or char == "*" or char == "+" or char == "(" or char == ")":
            if last_char != "%":
                new_regex += negation + char
                negation = ""
                last_char = char
            else:
                new_regex += "[" + negation + "\\" + char + "]"
                negation = ""
                last_char = ""
        # special characters in python regex syntax, need to be only characters
        elif char == "[" or char == "]" or char == "$" or char == "^" or char == "?" or char == "\\" \
                or char == "{" or char == "}":
            new_regex += "[" + negation + "\\" + char + "]"
            negation = ""
            last_char = char

        # whitespaces %t - tabs %n - newlines  %s - (" "\t\n\r\f\v)
        elif char == "t" or char == "n":
            if last_char != "%":
                new_regex += "[" + negation + char + "]"
                negation = ""
                last_char = char
            else:
                new_regex += "[" + negation + "\\" + char + "]"
                negation = ""
                last_char = ""
        elif char == "s":
            if last_char != "%":
                new_regex += "[" + negation + char + "]"
                negation = ""
                last_char = char
            else:
                new_regex += "[" + negation + " \t\n\r\f\v" + "]"
                negation = ""
                last_char = ""
        #  special regex %a - every character
        elif char == "a":
            if last_char != "%":
                new_regex += "[" + negation + char + "]"
                negation = ""
                last_char = char
            else:
                if negation == "":
                    new_regex += "."
                    negation = ""
                    last_char = ""
                else:
                    negation = ""
                    last_char = ""
        # %d one number between 0-9
        elif char == "d":
            if last_char != "%":
                new_regex += "[" + negation + char + "]"
                negation = ""
                last_char = char
            else:
                new_regex += "[" + negation + "0-9" + "]"
                negation = ""
                last_char = ""
        # %l one character between a-z
        elif char == "l":
            if last_char != "%":
                new_regex += "[" + negation + char + "]"
                negation = ""
                last_char = char
            else:
                new_regex += "[" + negation + "a-z" + "]"
                negation = ""
                last_char = ""
        # %L one character between A-Z
        elif char == "L":
            if last_char != "%":
                new_regex += "[" + negation + char + "]"
                negation = ""
                last_char = char
            else:
                new_regex += "[" + negation + "A-Z" + "]"
                negation = ""
                last_char = ""
        # %w one character between a-z or A-Z
        elif char == "w":
            if last_char != "%":
                new_regex += "[" + negation + char + "]"
                negation = ""
                last_char = char
            else:
                new_regex += "[" + negation + "a-zA-Z" + "]"
                negation = ""
                last_char = ""
        # %W one character between a-z or A-Z or number 0-9
        elif char == "W":
            if last_char != "%":
                new_regex += "[" + negation + char + "]"
                negation = ""
                last_char = char
            else:
                new_regex += "[" + negation + "a-zA-Z0-9" + "]"
                negation = ""
                last_char = ""
        # all other characters only copy into [character]
        else:
            if last_char != "%":
                new_regex += "[" + negation + char + "]"
                negation = ""
                last_char = char
            else:
                print("Bad format of fmt file, problem with this regular expression: " + reg, file=sys.stderr)
                exit(4)

    # recompile regex if is valid
    try:
        re.compile(new_regex)
    except re.error:
        print("Bad format of fmt file, problem with this regular expression: " + reg, file=sys.stderr)
        exit(4)
    return new_regex


def check_tag(tag):
    if tag == "bold" or tag == "italic" or tag == "teletype" or tag == "underline":
        pass
    elif tag.startswith("size:"):
        size = 0
        try:
            size = float(re.sub("size:", "", tag))
        except ValueError:
            print("Bad format of fmt file, problem in format command: " + tag, file=sys.stderr)
            exit(4)
        if size < 1.0 or size > 7.0:
            print("Bad format of fmt file, problem in format command: " + tag, file=sys.stderr)
            exit(4)
    elif tag.startswith("color:"):
        hex_num = int('000001', 16)
        try:
            hex_num = int(re.sub("color:", "", tag), 16)
        except ValueError:
            print("Bad format of fmt file, problem in format command: " + tag, file=sys.stderr)
            exit(4)
        if hex_num > int('FFFFFF', 16) or hex_num < int('000000', 16):
            print("Bad format of fmt file, problem in format command: " + tag, file=sys.stderr)
            exit(4)
    else:
        print("Bad format of fmt file, problem in format command: " + tag, file=sys.stderr)
        exit(4)


def parse_to_regex_tab_form(data):
    validated_output = []
    # iterate through data
    for line in data:
        # ignore blank lines
        if not line.isspace():
            # find regex
            regex = re.match("^(.*?)\t+", line)
            # ignore blank regex
            if regex is not None:
                form = re.sub(re.escape(regex.group()), "", line)  # returns all after regex group
                regex = re.sub("\t", "", regex.group())  # replace tabs with nothing
                regex = check_reg(regex)  # create from input regex valid regex
                form = [x.strip() for x in form.split(',')]  # removes whitespace and split separate by comma
                form = [x for x in form if x]  # removes empty strings
                if form:  # if is set some form
                    for tag in form:  # iterate through it
                        check_tag(tag)  # validate tag
                        validated_output.append({'regex': regex, 'form': form})  # append dictionary into list
    return validated_output

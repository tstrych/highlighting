#!/usr/bin/env python3.6

import argparse
import sys
import re
import io

import parser
import tagger


# prints help to user
def help_write():
    print("THIS IS HELP:")
    print()
    print("usage: python3.6 ./syn.py [--input=FILE]  [--output=FILE] [--format=FILE] [--br] OR --help")
    print("where:")
    print("        FILE is: path to the file with their name and extension")
    print("        Format : Format of format file need to be in format regex one or more tabs "
          "and format divided by coma and spaces or tabs of file")
    print()
    print("--br              add new line tag at the end of each line.")
    print("--input=FILE      input file.")
    print("--output=FILE     output file.")
    print("--format=FILE     format file.")
    print("--help            help information, already here")
    print()
    print("EXAMPLE:")
    print("         python3.6 ./syn.py --input=bar.in --output==foo.out --format=hello_world.fmt --br")
    sys.exit(0)


# arguments from arg parse, using output file and br option
# data which goes to output
def out(arguments, data):
    if arguments.out is not None:
        # try open file
        try:
            out_file = open(arguments.out[0], 'w')
        except IOError:
            print("Can't write to output file", file=sys.stderr)
            sys.exit(3)
    else:  # output argument was not set use standard output
        out_file = sys.stdout

    # insert br tags at the end of every line
    if arguments.br is not None:
        data = re.sub("\n", "<br />\n", data)

    # print data to output file without "/n" at the end
    print(data, file=out_file, end="")
    sys.exit(0)


# parse arguments
argv_parse = argparse.ArgumentParser(add_help=False)
argv_parse.add_argument('--help', action="count", dest="help")
argv_parse.add_argument('--input', action="append", default=None, dest="inp")
argv_parse.add_argument('--output', action="append", default=None, dest="out")
argv_parse.add_argument('--format', action="append", default=None, dest="form")
argv_parse.add_argument('--br', action="count", dest="br")


# try if was parsed good
try:
    argv = argv_parse.parse_args()
except SystemExit:
    print("Bad arguments", file=sys.stderr)
    sys.exit(1)

if argv.help is not None:
    if len(sys.argv) is 2:
        help_write()
    else:
        print("Need to use only param help", file=sys.stderr)
    sys.exit(1)


# control multiplicity of arguments
if argv.inp is not None and (len(argv.inp) > 1):
    print("Argument input was set multiple times", file=sys.stderr)
    sys.exit(1)

if argv.out is not None and (len(argv.out) > 1):
    print("Argument output was set multiple times", file=sys.stderr)
    sys.exit(1)

if argv.form is not None and (len(argv.form) > 1):
    print("Argument format was set multiple times", file=sys.stderr)
    sys.exit(1)

if int(argv.br or 0) > 1:
    print("Argument br was set multiple times", file=sys.stderr)
    sys.exit(1)


# standard input
if argv.inp is None:
    in_file_data = sys.stdin.read()
else:  # try open and read content of input file
    try:
        with open(argv.inp[0], 'r') as fi:
            in_file_data = fi.read()
    except IOError:
        print("Can't open file or read input file", file=sys.stderr)
        sys.exit(2)

# fmt file
if argv.form is not None:
    in_form_data = None
    try:  # try read fmt file set from arguments
        with open(argv.form[0], 'r') as ff:
            in_form_data = ff.read()
    except IOError:
        # problem with reading data, takes input to output without any change
        out(argv, in_file_data)

    # read goes right
    in_form_data = io.StringIO(in_form_data)  # data like string not like an object
    out_form_data = parser.parse_to_regex_tab_form(in_form_data)  # parse format file to regex and format
    out_file_data = tagger.create_tags(in_file_data, out_form_data)   # insert tags to input to get output
    out(argv, out_file_data)  # print output

# format file wasn't set, takes input to output without any change
else:
    out(argv, in_file_data)

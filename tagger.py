#!/usr/bin/env python3.6

import re


# returns right open tag
# form is list of form objects after regex in fmt file
def tag_open(form):
    tag = ""
    x = 0
    # iterate over whole form list because of multiple list control indexes
    for i, j in enumerate(form):
        if "size:" in j and x == i:
            length = len("size:")   # parse substring
            size = j[length:]   # take size
            tag += "<font size=" + size + ">"  # create tag
        elif "color:" in j and x == i:
            length = len("color:")   # parse substring
            color = j[length:]  # take color
            tag += "<font color=#" + color + ">"  # create tag
        elif "bold" in j and x == i:
            tag += "<b>"
        elif "italic" in j and x == i:
            tag += "<i>"
        elif "teletype" in j and x == i:
            tag += "<tt>"
        elif "underline" in j and x == i:
            tag += "<u>"
        x += 1
    return tag  # return open tag or open tags


# create close tags
# form is list of form objects after regex in fmt file
def tag_close(form):
    tag = ""
    x = len(form) - 1
    # iterate like in tag_open but in reverse order
    for i, j in reversed(list(enumerate(form))):
        if "size" in j and x == i:
            tag += "</font>"
        elif "color" in j and x == i:
            tag += "</font>"
        elif "bold" in j and x == i:
            tag += "</b>"
        elif "italic" in j and x == i:
            tag += "</i>"
        elif "teletype" in j and x == i:
            tag += "</tt>"
        elif "underline" in j and x == i:
            tag += "</u>"
        x -= 1
    return tag  # return close tag or close tags


# pos_counter
# form is list of form objects after regex in fmt file
# begin_pos, position where you want to give a tag
# positions list of all tags with position  with open and closed tags and
def pos_counter(form, begin_pos, positions):
    output_pos = begin_pos
    if "/" in form:  # choose open or closed tag
        for pos in positions:
            if begin_pos > pos["pos"]:
                output_pos += len(pos["form"])  # calculate right position
    else:
        for pos in positions:
            if begin_pos >= pos["pos"]:
                output_pos += len(pos["form"])  # calculate right position
    return output_pos


# data - output string where create tags insert strings
# form is list of form objects after regex in fmt file
def create_tags(data, form):
    positions = []
    flag = 0
    for i in form:
        if flag > 1:
            flag -= 1
        else:
            for note in re.finditer(i["regex"], data, re.DOTALL):
                if note.group(0) == "":
                    continue

                if len(i["form"]) > 1:
                    flag = len(i["form"])

                # count position for open tag
                pos_start = pos_counter(tag_open(i["form"]), note.start(), positions)
                # append dictionary to the list of positions with right tag and right position
                positions.append({"form": tag_open(i["form"]), "pos": note.start(), "position": pos_start})
                # do the same thing with close tag
                pos_end = pos_counter(tag_close(i["form"]), note.end(), positions)
                positions.append({"form": tag_close(i["form"]), "pos": note.end(), "position": pos_end})
    # iterate through position list and insert tags
    for position in positions:
        # insert string at right positions
        data = data[:position["position"]] + position["form"] + data[position["position"]:]
    return data

import os, sys
from rich import print

# so far these are mapped for the beginning values in steam.styles
# next will be mapping any lines with // comments
#
# some ideas:
# right now we're looking at ranges, this becomes less relevant later in
# the style doc. maybe mapping per-line-number in the future?
# { line_number : { doc_var : mapped_color } }
# pros: eliminates the need to parse, easy to read
# cons: slight changes in source will avalanche
#
# maybe putting color mappings in a template yaml for easier readability & changing???
# will look at this later ig


def color_swap_template(rgba_dict, path):
    """basically a mini-main for mapping & altering template colors"""

    # depending upon how many values end up being changed
    # dealing with color mappings might get unruly quickly
    # mapping them separately should allow for templating later
    map_background = rgba_dict["background"]
    map_foreground = rgba_dict["foreground"]
    map_black = rgba_dict["color0"]
    map_blue = rgba_dict["color4"]
    map_green = rgba_dict["color2"]
    map_cyan = rgba_dict["color6"]
    map_red = rgba_dict["color1"]
    map_purple = rgba_dict["color5"]
    map_yellow = rgba_dict["color3"]
    map_lblue = rgba_dict["color12"]
    map_lgreen = rgba_dict["color10"]
    map_lcyan = rgba_dict["color14"]
    map_lred = rgba_dict["color9"]
    map_lpurple = rgba_dict["color13"]
    map_lyellow = rgba_dict["color11"]
    map_lgray = rgba_dict["color7"]

    # changes some things for sure
    drac_color_dict = {
        "draculaSelection": map_blue,
        "draculaAccent": map_lcyan,
        "notificationColor": map_lpurple,
        "draculaCyan": map_cyan,
        "draculaGreen": map_lgreen,
        "draculaOrange": map_yellow,
        "draculaPink": map_lred,
        "draculaPurple": map_purple,
        "draculaRed": map_red,
        "draculaYellow": map_lyellow,
    }

    # not noticing a lot of changes with these
    general_color_dict = {
        "black": map_background,
        "dark": color_mod(map_background, intc=10),
        "almostBlack": color_mod(map_background, intc=5),
        "almostBlackTrans": color_mod(map_background, intc=10, alphac=-15),
        "white": map_foreground,
        "grey": color_mod(map_foreground, perc=-15),
        "none": (0, 0, 0, 0),
        "yellow": map_lyellow,
        "offwhite": color_mod(map_foreground, perc=-10),
        "dullgreen": map_green,
        "maize": map_yellow,
        "red": map_lred,
        "darkblue": map_blue,
        "blue": map_lblue,
        "darkred": map_red,
        "darkpurple": map_purple,
    }

    no_equals_color_dict = {
        "dark_blue": map_background,
        "med_blue": map_background,
        "bg_blue": map_background,
    }

    drac_list, general_list = gen_lines_list(drac_color_dict), gen_lines_list(
        general_color_dict
    )

    with open(path + "/resource/styles/steam.styles", "r") as f:
        template = f.readlines()

    template = modify_template(template, drac_list, (0, 23))
    template = modify_template(template, general_list, (24, 45))

    # write changes
    with open(path + "/resource/styles/steam.styles", "w") as f:
        f.writelines(template)


def gen_lines_list(color_dict):
    """transform color dict into writeable template lines"""

    gen_color_list = [
        f'      {k}     =   "{v[0]} {v[1]} {v[2]} {v[3]}"\n'
        for k, v in color_dict.items()
    ]

    return gen_color_list


def modify_template(template, lines_list, lines_num):
    """get appropriate template range and write list to template"""

    # get lines to change
    mod_list = list()
    for i, v in enumerate(template[lines_num[0] : lines_num[1]]):
        if v.__contains__("="):
            mod_list.append(i + lines_num[0])

    try:
        # modify template directly
        for i, v in enumerate(lines_list):
            template[mod_list[i]] = v
    except IndexError as e:
        print(
            f"index error!\nmod_list has {len(mod_list)} entries, while given lines list has {len(lines_list)} entries."
        )
        for i, v in enumerate(lines_list):
            print(f"LINE {i+1}: {v}", end="")
        for i in mod_list:
            print(f"{i}")
        for i in template[lines_num[0] : lines_num[1]]:
            print(f"{i}", end="")
        print(f"{e}")
        sys.exit(0)

    return template


def color_mod(color_tup, intc=0, perc=0, alphac=0):
    """manipulate color and transparency of rgba codes"""

    if intc != 0 and perc != 0:
        print("invalid inputs")
        return 0

    if perc != 0:
        change = round((perc / 100) * 255)
    else:
        change = intc

    new_color = list()

    for i in color_tup[0:3]:
        val = i + change
        if val > 255:
            val = 255
        elif val < 0:
            val = 0
        new_color.append(val)

    if alphac != 0:
        val = color_tup[3] + alphac
        if val > 255:
            val = 255
        elif val < 0:
            val = 0
        new_color.append(val)
    else:
        new_color.append(color_tup[3])

    return tuple(new_color)

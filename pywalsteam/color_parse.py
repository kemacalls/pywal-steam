import os
from PIL import ImageColor

COLOR_DICT = {
    "background": "",
    "foreground": "",
    "cursor": "",
    "color0": "",
    "color1": "",
    "color2": "",
    "color3": "",
    "color4": "",
    "color5": "",
    "color6": "",
    "color7": "",
    "color8": "",
    "color9": "",
    "color10": "",
    "color11": "",
    "color12": "",
    "color13": "",
    "color14": "",
    "color15": "",
}


def parse_file(path) -> tuple:
    """gets hex & rgba values from pywal's cache"""

    with open(path + "/colors.sh", "r") as f:
        contents = f.readlines()

    # shorten lines to just hex codes
    colors_trunc = [item[-9:-2] for item in contents]
    colors = list()

    # filter out irrelevant lines
    for i in colors_trunc:
        if len(i) > 0 and i[0] == "#" and i != "# Color":
            colors.append(i)

    hex_colors_dict = dict(zip(COLOR_DICT.keys(), colors))

    # rgba conversion
    for i, v in enumerate(colors):
        colors[i] = ImageColor.getcolor(v, "RGBA")

    rgba_colors_dict = dict(zip(COLOR_DICT.keys(), colors))

    # rgb conversion
    for i, v in enumerate(colors):
        colors[i] = colors[i][0:3]

    rgb_colors_dict = dict(zip(COLOR_DICT.keys(), colors))

    return hex_colors_dict, rgba_colors_dict, rgb_colors_dict

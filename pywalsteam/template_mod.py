import os, sys
import yaml
import re
import math
from rich import print
from PIL import Image, ImageDraw, ImageColor

def parse_steam_styles(rgba_dict, path):
    """turn color values from steam.styles into a dictionary"""
    with open(path + "/resource/styles/steam.styles", "r") as f:
        template = f.readlines()

    parsed_template = list()
    for i in template:
        # some entries are formatted without spaces
        val = re.findall('[A-z].+=[\s|"]\d.+\d.+\d.+\d.+["]', i)
        if len(val) > 0:
            parsed_template.append(val)
            continue
        # other entries are formatted with many spaces
        val2 = re.findall('[A-z]+\s+=\s+["]\d.+\d.+\d.+\d.+["]\\n', i)
        if len(val2) > 0:
            parsed_template.append(val2)

    parsed_template_dict = dict()
    for i in parsed_template:
        items = i[0].replace('"', "").replace("\t", " ").strip("\n").split("=")
        key = items[0].strip()
        value = items[1].strip().split(" ")
        value = [i for i in value if i.isdigit()]
        parsed_template_dict[key] = [int(i) for i in value]

    return parsed_template_dict


def preview_colorset(template_color_dict):
    """outputs a table image of scraped RGBA values (in RGB)"""
    color_dict = dict()
    for i, (k, v) in enumerate(template_color_dict.items()):
        color_dict[k] = ImageColor.getrgb(
            "rgb(" + str(v[0:3]).strip("[]").replace(" ", "") + ")"
        )

    max_per_col = 20
    col_len = 200
    w = round(len(color_dict) / 20) * col_len
    h = 20 * 21

    # making a transparent document
    img = Image.new("RGBA", (w, h))
    draw = ImageDraw.Draw(img)

    for i, (k, v) in enumerate(color_dict.items()):
        a, b, c, d, = (
            0,
            0 + (i + 1) % max_per_col * 20,
            20,
            20 + (i + 1) % max_per_col * 20,
        )
        # when reach max per column, create new column
        if (i / max_per_col) >= 1:
            a, c = a + (col_len * math.floor(i / max_per_col)), c + (
                col_len * math.floor(i / max_per_col)
            )
        draw.rectangle((a, b, c, d), fill=v)
        # drop shadow for readability
        draw.text((a + 31, d - 16), k, fill="#00000088")
        draw.text((a + 30, d - 17), k, fill="#ffffff")

    img.save("test.png")


def gen_lines_dict(color_dict):
    """transform modified color dict into writeable template lines"""
    lines_dict = dict()
    for key, val in color_dict.items():
        lines_dict[key] = f'      {key}     =   "{val[0]} {val[1]} {val[2]} {val[3]}"\n'

    return lines_dict


def read_template(path) -> list:
    """read template to lines"""
    with open(path, "r") as f:
        template = f.readlines()

    return template


def modify_template(template, lines_dict):
    """
    modify a given template based on a dictionary of modified lines.
    the key of lines_dict should reflect the line to be altered
    within the template.
    """

    for key, val in lines_dict.items():
        for index, item in enumerate(template):
            if item.__contains__(key):
                template[index] = val
                break

    return template


def write_template(template, path):
    """write template to file"""
    with open(path, "w") as f:
        f.writelines(template)

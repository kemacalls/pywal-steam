import os, sys
import yaml
import re
import math
from rich import print
from PIL import Image, ImageDraw, ImageColor

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

class ColorMap():
    def __init__(self, rgba_dict):
        self.bg = rgba_dict["background"]
        self.fg = rgba_dict["foreground"]
        self.black = rgba_dict["color0"]
        self.blue = rgba_dict["color4"]
        self.green = rgba_dict["color2"]
        self.cyan = rgba_dict["color6"]
        self.red = rgba_dict["color1"]
        self.purple = rgba_dict["color5"]
        self.yellow = rgba_dict["color3"]
        self.lblue = rgba_dict["color12"]
        self.lgreen = rgba_dict["color10"]
        self.lcyan = rgba_dict["color14"]
        self.lred = rgba_dict["color9"]
        self.lpurple = rgba_dict["color14"]
        self.lyellow = rgba_dict["color11"]
        self.lgray = rgba_dict["color7"]

def parse_template(rgba_dict, path):
    """turn color values from steam.styles into a dictionary"""
    with open(path + "/resource/styles/steam.styles", "r") as f:
        template = f.readlines()
    
    parsed_template = list()
    for i in template:
        # some entries are formatted without spaces
        val = re.findall('[A-z].+=[\s|"]\d.+\d.+\d.+\d.+["]',i)
        if len(val) > 0:
            parsed_template.append(val)
            continue
        # other entries are formatted with many spaces
        val2 = re.findall('[A-z]+\s+=\s+["]\d.+\d.+\d.+\d.+["]\\n',i)
        if len(val2) > 0:
            parsed_template.append(val2)
 
    parsed_template_dict = dict()
    for i in parsed_template:
        items = i[0].replace('"','').replace("\t",' ').strip("\n").split("=")
        key = items[0].strip()
        value = items[1].strip().split(' ')
        value = [ i for i in value if i.isdigit() ]
        parsed_template_dict[key] = [ int(i) for i in value ]

    return parsed_template_dict

def preview_colorset(template_color_dict):
    """outputs an table image of scraped RGBA values (in RGB)"""
    color_dict = dict()
    for i, (k,v) in enumerate(template_color_dict.items()):
        color_dict[k] = ImageColor.getrgb("rgb("+str(v[0:3]).strip("[]").replace(" ","")+")")

    max_per_col = 20
    col_len = 200
    w = round(len(color_dict) / 20) * col_len
    h = 20 * 21

    # making a transparent document
    img = Image.new("RGBA", (w, h))
    draw = ImageDraw.Draw(img)

    for i, (k, v) in enumerate(color_dict.items()):
        a, b, c, d, = 0, 0 + (i+1)%max_per_col * 20, 20, 20 + (i+1)%max_per_col * 20 
        # when reach max per column, create new column
        if (i/max_per_col) >= 1:
            a, c = a + (col_len * math.floor(i/max_per_col)), c + (col_len * math.floor(i/max_per_col))
        draw.rectangle((a,b,c,d), fill = v)
        # drop shadow for readability
        draw.text((a+31,d-16), k, fill="#00000088")
        draw.text((a+30,d-17), k, fill="#ffffff")

    img.save("test.png")

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

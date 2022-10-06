import os, sys
from rich import print

def color_swap_template(rgba_dict, path):

    drac_color_dict = {
        "draculaSelection" : rgba_dict['color9'],
        "draculaAccent" : rgba_dict['color15'],
        "notificationColor" : rgba_dict['color14'],
        "draculaCyan" : rgba_dict['color10'],
        "draculaOrange" : rgba_dict['color11'],
        "draculaPink" : rgba_dict['color12'],
        "draculaPurple" : rgba_dict['color13'],
        "draculaRed" : rgba_dict['color14'],
        "draculaYellow" : rgba_dict['color15'],
    }

    drac_color_list = [ f"      {k}     =   \"{v[0]} {v[1]} {v[2]} {v[3]}\"\n" for k, v in drac_color_dict.items() ]

    with open(path + '/resource/styles/steam.styles', 'r') as f:
        template = f.readlines()

    # get lines to change
    mod_list = list()
    for i, v in enumerate(template[0:23]):
        if v.__contains__("="):
            mod_list.append(i)

    # modify template directly
    for i, v in enumerate(drac_color_list):
        template[mod_list[i]] = v

    # write changes
    with open(path + '/resource/styles/steam.styles', 'w') as f:
        f.writelines(template)


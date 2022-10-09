from color_parse import *
from template_mod import *
from validation import *
from rich import print


def main():
    # paths are correct
    valid_dirs = validate_paths()
    # get back the color dict format we want from pywal
    _, rgba_dict, _ = parse_file(valid_dirs["pywal"])
    # parse out the default color keys/values from steam.styles
    pt_dict = parse_steam_styles(rgba_dict, valid_dirs["dracula"])
    # turn them all red so i can See
    # for k, v in pt_dict.items():
    #    pt_dict[k] = [255, 0, 0, 255]
    # display them in a little table image
    preview_colorset(pt_dict)
    # format the changed values into writebale template lines
    lines_dict = gen_lines_dict(pt_dict)
    # fetch the template for r/w
    steam_styles_path = valid_dirs["dracula"] + "/resource/styles/steam.styles"
    template = read_template(steam_styles_path)
    # modify the template with the color dict we made
    modify_template(template, lines_dict)
    # write the changes
    write_template(template, steam_styles_path)


if __name__ == "__main__":
    main()

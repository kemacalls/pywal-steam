from color_parse import *
from template_mod import *
from validation import *
from rich import print


def main():
    valid_dirs = validate_paths()
    _, rgba_dict, _ = parse_file(valid_dirs["pywal"])
    pdt = parse_template(rgba_dict, valid_dirs["dracula"])
    preview_colorset(pdt)


if __name__ == "__main__":
    main()

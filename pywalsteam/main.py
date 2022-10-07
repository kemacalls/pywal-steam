from color_parse import *
from template_mod import *
from validation import *
from rich import print


def main():
    valid_dirs = validate_paths()
    _, rgba_dict, _ = parse_file(valid_dirs["pywal"])
    color_swap_template(rgba_dict, valid_dirs["dracula"])


if __name__ == "__main__":
    main()

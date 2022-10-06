from color_parse import *
from validation import *
from rich import print

def main():
    valid_dirs = validate_paths()
    a, b, c = parse_file(valid_dirs['pywal'])
    print(a, b, c)

if __name__ == "__main__":
    main()
from color_parse import parse_file
from rich import print

def main():
    a, b, c = parse_file()
    print(a, b, c)

if __name__ == "__main__":
    main()
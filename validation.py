import os, sys
import yaml
from rich.prompt import Prompt, Confirm

USER_HOME = os.path.expanduser('~')
PYWAL_DEFAULT_DIR = USER_HOME + '/.cache/wal'
STEAM_DEFAULT_DIR = USER_HOME + '/.local/share/Steam'
THEME_DEFAULT_DIR = STEAM_DEFAULT_DIR + '/skins/Dracula'
DIR_DICT = {
    'pywal'   : PYWAL_DEFAULT_DIR,
    'steam'   : STEAM_DEFAULT_DIR,
    'dracula' : THEME_DEFAULT_DIR,
}

with open(os.getcwd() + '/config/paths.yaml', 'r') as f:
    paths_config = yaml.safe_load(f)
for k, v in paths_config.items():
    if v != 'default':
        DIR_DICT[k] = v

def main():
    validate_paths()

def define_custom_dir(dir, default) -> str:
    '''let user create custom directories'''

    conf = Confirm.ask(f"could not find {dir}'s directory. would you like to define a non-default path for this directory?")
    if conf is False: 
        sys.exit()
    
    while True:
        nd_path = Prompt.ask(f"enter path for {dir} (default: {default})")

        if os.path.exists(nd_path):
            print(f"{dir} ok!")
            DIR_DICT[k] = nd_path
            with open(os.getcwd() + '/config/paths.yaml', 'w') as f:
                yaml.safe_dump(DIR_DICT, f)
            return nd_path
        else:
            print(f"{nd_path} was invalid! try again...")

def validate_paths() -> dict:
    '''ensure all paths are present'''
    
    try:
        for k, v in DIR_DICT.items():
            if os.path.exists(v):
                print(f"{k} ok!")
            else: 
                DIR_DICT[k] = define_custom_dir(k, v)
        return DIR_DICT
    except Exception as e:
        print(f"path checks failed!\n{e}")
        sys.exit(0)
        

if __name__ == "__main__":
    main()
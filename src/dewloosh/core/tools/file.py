import os


def desktopfolder():
    return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')


def dir_name_ext(fullpath: str):
    dirpath, filename = os.path.split(fullpath)
    name, ext = filename.split(".")
    return dirpath, name, ext


def fullpath_to_dir(fullpath: str):
    return dir_name_ext(fullpath)[0]


def fullpath_to_name(fullpath: str):
    return dir_name_ext(fullpath)[1]


def fullpath_to_ext(fullpath: str):
    return dir_name_ext(fullpath)[2]

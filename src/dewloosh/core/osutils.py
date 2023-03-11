import os
import inspect


def find_source_folder(current_file:str=None, maxlevel:int=10) -> str:
    """
    Returns the source folder.
    """
    if current_file is None:
        current_file = __file__
    
    parent_is_src = False
    for _ in range(maxlevel):
        parent_is_src = os.path.dirname(current_file).endswith('src')
        if parent_is_src:
            break
        else:
            current_file = os.path.dirname(current_file)
    
    if parent_is_src:
        return os.path.dirname(current_file)
    else:
        raise RuntimeError
    

def get_definition_file_path(obj):
    """
    Returns the path of the file a class or a function is implemented in.
    """
    if inspect.isfunction(obj) or inspect.ismethod(obj):
        file_path = inspect.getfile(obj)
    elif inspect.isclass(obj):
        file_path = inspect.getfile(obj.__class__)
    else:
        raise ValueError("Input must be a function or class.")
        
    return os.path.abspath(file_path)
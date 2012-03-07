import os

def expand(d):
    return os.path.abspath(os.path.expanduser(os.path.expandvars(d)))

def get_or_create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path
 
def whereis(program):
    for path in os.environ.get('PATH', '').split(':'):
        if os.path.exists(os.path.join(path, program)) and \
           not os.path.isdir(os.path.join(path, program)):
            return os.path.join(path, program)
    return None

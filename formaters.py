# Refactor the name of the directory to avoid errors and convert it to a valid name
def refactorDirName(dir_name):
    return dir_name.replace(' ', '_').replace(':', '').replace('?', '').replace('¿', '').replace('¡', '').replace('!', '') 
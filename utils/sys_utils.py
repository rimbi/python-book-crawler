from os import getcwd

def FindRootPath():
    dirlist = getcwd().split('/')
    index = dirlist.index('kitapsever')
    return "/".join(dirlist[:index + 1])

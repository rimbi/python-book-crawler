from os import getcwd

def FindRootPath():
    dirlist = getcwd().split('/')
    index = dirlist.index('bookcrawler')
    return "/".join(dirlist[:index + 1])

# coding: utf-8

def getfilelines(filename, eol='\n', buffsize=4096):
    """计算给定文件有多少行"""
    with open(filename, 'rb') as handle:
        linenum = 0
        buffer = handle.read(buffsize)
        while buffer:
            linenum += buffer.count(eol)
            buffer = handle.read(buffsize)
        return linenum

def readtline(filename, lineno, eol="\n", buffsize=4096):
    """读取文件的指定行"""
    with open(filename, 'rb') as handle:
        readedlines = 0
        buffer = handle.read(buffsize)
        while buffer:
            thisblock = buffer.count(eol)
            if readedlines < lineno < readedlines + thisblock:
                # inthisblock: findthe line content, and return it
                return buffer.split(eol)[lineno - readedlines - 1]
            elif lineno == readedlines + thisblock:
                # need continue read line rest part
                part0 = buffer.split(eol)[-1]
                buffer = handle.read(buffsize)
                part1 = buffer.split(eol)[0]
                return part0 + part1
            readedlines += thisblock
            buffer = handle.read(buffsize)
        else:
            raise IndexError

def getrandomline(filename):
    """读取文件的任意一行"""
    import random
    return readtline(
        filename,
        random.randint(0, getfilelines(filename)),
    )

# if __name__ == "__main__":
#     import sys
#     import os
#     if len(sys.argv) == 1:
#         print getrandomline("file.csv")
#     else:
#         for f in filter(os.path.isfile, sys.argv[1:]):
#             print getrandomline(f)
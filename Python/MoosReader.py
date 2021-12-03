#!/usr/bin/env python
def MoosReader(moos_file,app):
    block = []
    dic = {}
    with open(moos_file, 'r') as f:
        text = f.readlines()
        block_found = False
        begin = False
        end = False
        for line in text:
            if line.startswith('MOOSTimeWarp'):
                block.append(line)
            if line.startswith('ServerPort'):
                block.append(line)
            if line=="ProcessConfig = " +app+ "\n":
                block_found=True
            if (line=='{\n' and block_found == True):
                begin=True
            if (line=='}\n' and begin == True):
                end=True
            if (begin==True and end == False):
                block.append(line)
    for line in block:
        res=[0,0]
        res = line.split('=')
        if len(res)>1:
            dic[res[0].strip(' ')] = float(res[1])
    return dic

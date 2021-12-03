import numpy as np
import os


def write_bhv(path,posf,vname):
    # gen new lines
    polygon = "polygon ="
    for wp in path:
        polygon+=f" {wp[0]},{wp[1]} :"
    polygon=polygon[:-1]
    polygon+="\n"
    station_pt = f"station_pt = {posf[0]}, {posf[1]} \n"
    # find and modify lines
    text=[]
    with open("model_ship.bhv", 'r') as f:
        text = f.readlines()
        for line in text:
            if "polygon" in line:
                idx=text.index(line)
                text[idx] = polygon
            if "station_pt" in line:
                idx=text.index(line)
                text[idx] = station_pt
    #  write new file
    new_file=vname+".bhv"
    with open(new_file, 'w') as f:
        f.writelines(text)

def write_moos(pos0,origem, hdg, vname, ships):
    # gen new lines
    LatOrigin = f"LatOrigin = {origem[0]} \n"
    LongOrigin = f"LongOrigin = {origem[1]} \n"
    START_X = f"START_X = {pos0[0]} \n"
    START_Y = f"START_Y = {pos0[1]} \n"
    START_HEADING = f"START_HEADING = {hdg} \n"
    ServerPort = f"ServerPort = {9000 + ships.index(vname) + 1} \n"
    Community = f"Community  = {vname}\n"
    pshare_input = f"input = route =  localhost:{9200+ ships.index(vname) + 1}\n"
    behaviors = f"behaviors  = {vname}.bhv\n"
    # find and modify lines
    text=[]
    with open("model_ship.moos", 'r') as f:
        text = f.readlines()
        for line in text:
            if "LatOrigin" in line:
                idx=text.index(line)
                text[idx] = LatOrigin
            if "LongOrigin" in line:
                idx=text.index(line)
                text[idx] = LongOrigin
            if "ServerPort" in line:
                idx=text.index(line)
                text[idx] = ServerPort
            if "Community" in line:
                idx=text.index(line)
                text[idx] = Community
            if "input" in line:
                idx=text.index(line)
                text[idx] = pshare_input
            if "behavior" in line:
                idx=text.index(line)
                text[idx] = behaviors
            if "START_X" in line:
                idx=text.index(line)
                text[idx] = START_X
            if "START_Y" in line:
                idx=text.index(line)
                text[idx] = START_Y
            if "START_HEADING" in line:
                idx=text.index(line)
                text[idx] = START_HEADING
    #  write new file
    new_file=vname+".moos"
    with open(new_file, 'w') as f:
        f.writelines(text)

def write_ms(origem):
    # gen new lines
    LatOrigin = f"LatOrigin = {origem[0]} \n"
    LongOrigin = f"LongOrigin = {origem[1]} \n"
    # find and modify lines
    text=[]
    with open("model_mothership.moos", 'r') as f:
        text = f.readlines()
        for line in text:
            if "LatOrigin" in line:
                idx=text.index(line)
                text[idx] = LatOrigin
            if "LongOrigin" in line:
                idx=text.index(line)
                text[idx] = LongOrigin
    #  write new file
    new_file="mothership.moos"
    with open(new_file, 'w') as f:
        f.writelines(text)

def write_sh(vnames):
    # find and modify lines
    end = False
    text=[]
    with open("model_launch.sh", 'r') as f:
        text = f.readlines()
        for line in text:
            if "pAntler" in line and not end:
                idx=text.index(line)
                for vname in vnames:
                    # gen new lines
                    launch = f" pAntler {vname}.moos --MOOSTimeWarp=$TIME_WARP >& /dev/null & \n"
                    text.insert(idx+vnames.index(vname)+1,launch)
                end = True
    new_file="launch.sh"
    with open(new_file, 'w') as f:
        f.writelines(text)


def run():
    cmd = 'gnome-terminal -- chmod +x launch.sh'
    os.system(cmd)
    cmd = 'gnome-terminal -- ./launch.sh'
    os.system(cmd)
        
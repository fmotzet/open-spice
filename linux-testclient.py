import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

import subprocess
import json
import pprint
pp= pprint.PrettyPrinter(indent=4)

flavorcommand = "hostnamectl"
command = "nixos-option environment.systemPackages"
usercommand = "whoami"
softwarecommand = {"rhel":"rpm --query --all --info",  "flatpak":"flatpak list --app --columns=appocation | head -n-1", "nixos": "nixos-option environment.systemPackages", "others":"/user/local"}

def runAndConvert(rccommand):
    myp = subprocess.run(rccommand, capture_output=True, shell=True)
    myd = myp.stdout.decode().split("\n")
    mydd = {}
    for x in myd:
        if x:
            mydd[str(x.split(":")[0]).strip()] = x.split(":")[1].strip()
    return mydd

def collector():
    finalDict = {}
    finalDict.update(runAndConvert(flavorcommand))
    return(finalDict)

if type(collector()) == dict or list:
    myCoolInfo = json.dumps(collector())
else:
    print("wrong type")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        mystring = input("Enter something:")
        if mystring == "you":
            mystring = myCoolInfo
            print((myCoolInfo).encode())
            s.sendall((myCoolInfo).encode("utf-8"))
        elif mystring == "done":
            break
        else:
            s.sendall((mystring).encode("utf-8"))
        data = s.recv(1024)

        if data == (b"terminting connection"):
            print(data)
            break
        #print(data)

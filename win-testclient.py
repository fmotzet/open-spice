import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

import subprocess
import json
import pprint
pp= pprint.PrettyPrinter(indent=4)

softwareCommands = ["Get-ChildItem -Path HKLM:SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall | Get-ItemProperty | Sort-Object -Property DisplayName | Select-Object -Property DisplayName, DisplayVersion, InstallDate, InstallLocation | ConvertTo-Json",
            "Get-ChildItem -Path HKCU:Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall | Get-ItemProperty | Sort-Object -Property DisplayName | Select-Object -Property DisplayName, DisplayVersion, InstallDate, InstallLocation | ConvertTo-Json",
            "Get-ChildItem -Path HKLM:Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall | Get-ItemProperty | Sort-Object -Property DisplayName | Select-Object -Property DisplayName, DisplayVersion, InstallDate, InstallLocation | ConvertTo-Json",]
computerNameCommand = "Get-ItemProperty HKLM:SYSTEM\\CurrentControlSet\\Control\\ComputerName\\ComputerName | Get-ItemProperty | Sort-Object | Select-Object -Property ComputerName | ConvertTo-Json"
windowsInfoCommand = "Get-ItemProperty 'HKLM:SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion' | Get-ItemProperty | Sort-Object | Select-Object -Property CompositionEditionID, CurrentBuild, DisplayVersion, RegisteredOrganization, RegisteredOwner | ConvertTo-Json"
def runAndConvert(command):
    myp = subprocess.Popen(["powershell", command],shell=True, stdout=subprocess.PIPE)
    myb = (myp.stdout.read()).decode('utf-8)')
    myo = json.loads(myb)
    return myo

def collector():
    allSoftware = []
    for mycommand in softwareCommands:
        for innerdict in runAndConvert(mycommand):
            if innerdict["DisplayName"] == None:
                continue
            else:
                allSoftware.append(innerdict)
    thisComputerName = runAndConvert(computerNameCommand)
    thisWinInfo = runAndConvert(windowsInfoCommand)
    
    finalDict = {thisComputerName['ComputerName']:[thisWinInfo,allSoftware]}
    
    #print (finalDict)
    # print(type(allSoftware))
    # pp.pprint(thisComputerName)
    # pp.pprint(thisWinInfo)
    # pp.pprint(allSoftware)
    return(finalDict)

if type(collector()) == dict or list:
    myWinInfo = json.dumps(collector())
else:
    print("wrong type")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        mystring = input("Enter something:")
        if mystring == "you":
            mystring = myWinInfo
            print(json.dumps(myWinInfo).encode())
            s.sendall(json.dumps(myWinInfo).encode("utf-8"))
        elif mystring == "done":
            break
        else:
            s.sendall((mystring).encode("utf-8"))
        data = s.recv(1024)

        if data == (b"terminting connection"):
            print(data)
            break
        #print(data)

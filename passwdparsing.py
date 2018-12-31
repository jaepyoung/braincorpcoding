import sys
import unittest
import json
import argparse



## Define exception for wrong file format 
class Error(Exception):
   """Base class for other exceptions"""
   pass

class FileFormatNotCorrect(Error):
   """Raised when the input value is too small"""
   pass

# Function of open file.    
def openfiles(filepath):
    filepathfh=""
    try: 
        filepathfh = open(filepath,'r')
    except FileNotFoundError:
        print(filepath+"Not found")
        raise
    return filepathfh

# Getting the list of keys of dictionary with given value    
def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if valueToFind in item[1]:
            listOfKeys.append(item[0])
    return  listOfKeys

# Getting groupname with given guid. 
def getgroupfromgui(guid,groupfile):
    groupfilefh = openfiles(groupfile)
    groupname=""
    for line in groupfilefh:
        if not line.startswith("#"):
            linelist=line.split(":")
            if linelist[2]==guid:
                groupname = linelist[0]
    return groupname

# Main function 
def passwordmerge(passwdfile, groupfile):
    # Assiginging default values if the values are not provided. 
    if passwdfile is None: 
        passwdfile="/etc/passwd"
    if groupfile is None: 
        groupfile="/etc/group"

    passwdfilefh = openfiles(passwdfile)
    groupfilefh = openfiles(groupfile)
    groups={}
    users={}
    for line in groupfilefh:
        if not line.startswith("#"):
            linelist  = line.split(":")
            if len(linelist) > 5 or len(linelist) <2: 
                raise FileFormatNotCorrect("It is not group file")
            if linelist[3] is not None:
                groups[linelist[0]]=linelist[3]
            else:
                groups[linelist[0]]="" 

    for line in passwdfilefh:
        if not line.startswith("#"):
            linelist = line.split(":")
            if len(linelist) < 6: 
                raise FileFormatNotCorrect("It is not passwd file")
            grouplist=getKeysByValue(groups,linelist[0])
            users[linelist[0]]={}
            users[linelist[0]]["uid"] = linelist[2]
            users[linelist[0]]["full_name"] = linelist[4]
            grouplist.append(getgroupfromgui(linelist[3],groupfile))
            users[linelist[0]]["groups"]= grouplist
            grouplist=[]
    json_data = json.dumps(users)
    print(json_data)
    return json_data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--passwd',help='path of passwd file')
    parser.add_argument('--group',help='path of group file')
    args = parser.parse_args()
    passwdfile=args.passwd
    groupfile=args.group
    passwordmerge(passwdfile, groupfile)

class TestStringMethods(unittest.TestCase):
    def test_exceptiong_notfoundpasswordfile(self):
        with self.assertRaises(FileNotFoundError):
            passwordmerge("incorrect","./testgroup") 
    def test_exceptiong_notfoundgroupfile(self):
        with self.assertRaises(FileNotFoundError):
            passwordmerge("/etc/passwd","incorretgroup")  
    def test_exceptiong_notwrongpasswdformatfile(self):
        with self.assertRaises(FileFormatNotCorrect):
            passwordmerge("/etc/hosts","/etc/group") 
    def test_exceptiong_notwronggroupfile(self):
        with self.assertRaises(FileFormatNotCorrect):
            passwordmerge("/etc/passwd","/etc/hosts")  
    def test_filesnotprovided(self):
        self.assertEqual(passwordmerge(None,None),passwordmerge("/etc/passwd","/etc/group"))  
    def test_paswdfilenotproivide(self):
        self.assertEqual(passwordmerge("/etc/passwd",None),passwordmerge("/etc/passwd","/etc/group"))  
    def test_groupfilenotprovided(self):
        self.assertEqual(passwordmerge(None,"/etc/group"),passwordmerge("/etc/passwd","/etc/group"))      
    def test_testgroup_testpasswd_fileschecking(self):
        a=json.loads("""
        {
            "root": {"uid": "0", "full_name": "root", "groups": ["root"]},
            "nobody": {"uid": "65534", "full_name": "nobody", "groups": ["nogroup"]}, 
            "systemd-bus-proxy": {"uid": "103", "full_name": "systemd Bus Proxy,,,", "groups": ["systemd-bus-proxy"]}, 
            "ntp": {"uid": "104", "full_name": "", "groups": ["ntp"]}, 
            "statd": {"uid": "105", "full_name": "", "groups": ["nogroup"]}, 
            "sshd": {"uid": "106", "full_name": "", "groups": ["nogroup"]}, 
            "admin": {"uid": "1000", "full_name": "Debian", "groups": ["adm", "dialout", "cdrom", "floppy", "audio", "dip", "video", "plugdev", "admin"]}
        }
        """)
        self.assertEqual(a,json.loads(passwordmerge("./testpasswd","./testgroup")))
    


if __name__ == '__main__':
    main()
    
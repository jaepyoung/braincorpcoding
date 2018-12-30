import sys
import unittest
import json

# Getting parameter for password file and group file 
#passwdfile = sys.argv[1] 
#groupfile = sys.argv[2] 
# def parse_args(args):

def openfiles(filepath):
    filepathfh=""
    try: 
        filepathfh = open(filepath,'r')
    except FileNotFoundError:
        print(filepath+" doesn't exist")
    return filepathfh

    
def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if valueToFind in item[1]:
            listOfKeys.append(item[0])
    return  listOfKeys

def getgroupfromgui(guid,groupfile):
    groupfilefh = openfiles(groupfile)
    groupname=""
    for line in groupfilefh:
        if not line.startswith("#"):
            linelist=line.split(":")
            if linelist[2]==guid:
                groupname = linelist[0]
    return groupname


def passwordmerge(passwdfile, groupfile,mode):
    if mode!="unittest":
        passwdfile = sys.argv[1] 
        groupfile = sys.argv[2] 
    
    # Assiginging default values
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
                print("This is not group file")
                return
            if linelist[3] is not None:
                groups[linelist[0]]=linelist[3]
            else:
                groups[linelist[0]]="" 

    for line in passwdfilefh:
        if not line.startswith("#"):
            linelist = line.split(":")
            if len(linelist) < 6: 
                print("This is not group file")
                return
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
    passwdfile=""
    groupfile=""
    mode="prod"
    passwordmerge(passwdfile, groupfile,mode)

class TestStringMethods(unittest.TestCase):
    #def test_checking_filesformat(self):
    #    self.assertRaises(FileNotFoundError, passwordmerge("test","test","unittest"))
    #def test_print_fileformats(self):
    #    self.assertTrue(passwordmerge("/etc/passwd","test","unittest"))
    def test_print_fileformats2(self):
        self.assertTrue(passwordmerge("/etc/passwd","/etc/group","unittest"))
    def test_print_fileformats3(self):
        self.assertTrue(passwordmerge("./testpasswd","./testgroup","unittest"))


if __name__ == '__main__':
    main()
    
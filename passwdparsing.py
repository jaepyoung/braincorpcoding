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
            groups[linelist[0]]=linelist[3]

    for line in passwdfilefh:
        if not line.startswith("#"):
            linelist = line.split(":")
            users[linelist[0]] = ["uid:"+linelist[1], "full_name:"+linelist[4],"groups:"] 
    json_data = json.dumps(users)
    print(json_data)
    return json_data
class TestStringMethods(unittest.TestCase):
    #def test_checking_filesformat(self):
    #    self.assertRaises(FileNotFoundError, passwordmerge("test","test","unittest"))
    def test_print_fileformats(self):
        self.assertTrue(passwordmerge("/etc/passwd","test","unittest"))
    def test_print_fileformats2(self):
        self.assertTrue(passwordmerge("/etc/passwd","/etc/group","unittest"))


if __name__ == '__main__':
    unittest.main()
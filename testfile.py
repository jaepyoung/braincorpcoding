import unittest
from passwdparsing import passwdparsing


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
    unittest.main()

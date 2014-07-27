# pyJConf unit tests

import unittest
import os
import exceptions

from pyJConf import JConf
from pyJConf import SettingUnspecifiedError, JConfSyntaxError, JConfRecursiveFileError

class TestSettingsLoad(unittest.TestCase):
    def setUp(self):
        file_one = """// This is a comment
{"defsettinga": "foo",
"defsettingb": "bar"

@user, "usersetting": "A"
}"""

        f = open("temp_file_one.jconf", 'w+')
        f.write(file_one)
        f.close()

        file_two = """{
        "setting": A"
}"""

        f = open("temp_file_two.jconf", 'w+')
        f.write(file_two)
        f.close()

        file_three = """{
        "setting": "A",
@user "usersetting": 5,
include(temp_extra.jconf)
@user include(user_extra.jconf)
}"""

        f = open("temp_file_three.jconf", 'w+')
        f.write(file_three)
        f.close()

        file_four = """
"extralist": [7, 8, 9]
"""

        f = open("temp_extra.jconf", 'w+')
        f.write(file_four)
        f.close()

        file_five = """
include(user_extra2.jconf)
"""

        f = open("user_extra.jconf", 'w+')
        f.write(file_five)
        f.close()

        file_six = """
,"usernested": "Hello"
"""

        f = open("user_extra2.jconf", 'w+')
        f.write(file_six)
        f.close()

        file_seven = """
{"A": 5,
include(temp_recursiveB.jconf)
}
"""

        f = open("temp_recursive.jconf", 'w+')
        f.write(file_seven)
        f.close()

        file_eight = """
include(temp_recursive.jconf)
"""

        f = open("temp_recursiveB.jconf", 'w+')
        f.write(file_eight)
        f.close()


    def test_loaddefault_implicit(self):
        s = JConf("temp_file_one.jconf")
        self.assertTrue(s.defsettinga == 'foo')
        self.assertTrue(s.defsettingb == 'bar')
        with self.assertRaises(SettingUnspecifiedError):
            len(s.usersetting)


    def test_loaddefault_explicit(self):
        s = JConf("temp_file_one.jconf", "default")
        self.assertTrue(s.defsettinga == 'foo')
        self.assertTrue(s.defsettingb == 'bar')
        with self.assertRaises(SettingUnspecifiedError):
            len(s.usersetting)


    def test_loaduser(self):
        s = JConf("temp_file_one.jconf", "user")
        self.assertTrue(s.defsettinga == 'foo')
        self.assertTrue(s.defsettingb == 'bar')
        self.assertTrue(s.usersetting == 'A')


    def test_JSONissue(self):
        with self.assertRaises(JConfSyntaxError):
            s = JConf("temp_file_two.jconf")


    def test_nested(self):
        s = JConf("temp_file_three.jconf")
        self.assertTrue(s.setting == 'A')
        self.assertTrue(s.extralist == [7, 8, 9])


    def test_nestedinclude(self):
        s = JConf("temp_file_three.jconf", "user")
        self.assertTrue(s.setting == 'A')
        self.assertTrue(s.extralist == [7, 8, 9])
        self.assertTrue(s.usernested == "Hello")


    def test_recursiveerror(self):
        with self.assertRaises(JConfRecursiveFileError):
            s = JConf("temp_recursive.jconf")


    def tearDown(self):
        os.remove("temp_file_one.jconf")
        os.remove("temp_file_two.jconf")
        os.remove("temp_file_three.jconf")
        os.remove("temp_extra.jconf")
        os.remove("user_extra.jconf")
        os.remove("user_extra2.jconf")
        os.remove("temp_recursive.jconf")
        os.remove("temp_recursiveB.jconf")

if __name__ == '__main__':
    unittest.main()
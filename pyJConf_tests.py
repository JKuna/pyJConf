# pyJConf unit tests

import unittest
import os
import exceptions

from pyJConf import JConf, SettingUnspecifiedError

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


    def tearDown(self):
        os.remove("temp_file_one.jconf")


if __name__ == '__main__':
    unittest.main()
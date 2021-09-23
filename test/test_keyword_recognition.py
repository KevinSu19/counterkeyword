import unittest
import sys
sys.path.insert(0, "../code")
from keyCount import *


# Test a few key functions
class MyTestCase(unittest.TestCase):
    def test_clean_data(self):
        str1 = "/*sss*/ 'dd'"
        str_ans1 = "            "
        str2 = "/*ddddd \n*/"
        str_ans2 = "           "
        str3 = '"xxsubtxxxy"'
        str_ans3 = "            "
        self.assertEqual(clean_data(str1), str_ans1)
        self.assertEqual(clean_data(str2), str_ans2)
        self.assertEqual(clean_data(str3), str_ans3)

    def test_key_count(self):
        text = read_file("../data/key.c")
        temp, num = key_count(text)
        self.assertEqual(num, 35)

    def test_switch_case_count(self):
        key_data = ['include', 'stdio', 'int', 'main', 'int', 'double', 'long', 'switch',
                    'case', 'break', 'case', 'break', 'case', 'break', 'default', 'break',
                    'switch', 'case', 'break', 'case', 'break', 'default', 'break', 'if',
                    'if', 'else', 'else', 'if', 'if', 'else', 'if', 'else', 'if', 'else',
                    'else', 'if', 'else', 'return']
        switch_num, case_num = switch_case_count(key_data)
        self.assertEqual(switch_num, 2)
        self.assertEqual(case_num, [3, 2])

    def test_if_else_count(self):
        text = read_file("../data/text.c")
        if_else_num = if_else_count(text)
        self.assertEqual(if_else_num, 4)

    def test_if_elseif_else_count(self):
        text = read_file("../data/key.c")
        temp, if_elseif_else_num = if_elseif_else_count(text)
        self.assertEqual(if_elseif_else_num, 2)


if __name__ == '__main__':
    unittest.main()

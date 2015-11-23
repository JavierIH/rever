import unittest
from rever.robot.rever import Rever


class Test(unittest.TestCase):

    def testName(self):
        robot = Rever(l1=10, l2=10)

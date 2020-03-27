#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest, platform


class Action():
    def action_test(self,step_list):
        runner = Runner()
        if step_list == 1:
            runner.test_exportVideo()
        elif step_list == 2:
            runner.test_exportGif()
        else:
            runner.test_exportMP3()

    @staticmethod
    def generateTest(step_list):
        # print "step_list.. {}".format(step_list)
        def func(self):
            self.action_test(step_list)
        return func


class Runner(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print "setUpClass"

    @classmethod
    def tearDownClass(cls):
        #         "Hook method for deconstructing the class fixture after running all tests in the class."
        print("\n\n---------------------------------------tearDownClass----------------------------------------")
        pass

    def setUp(self):
        print("\n-------------setUp------------\n")
        pass

    def tearDown(self):
        print("\n-------------tearDown------------\n")
        pass

    def test_exportVideo(self):
        print("\n-------------test_exportVideo------------\n")
  
    def test_exportGif(self):
        print("\n-------------test_exportGif------------\n")
  
    def test_exportMP3(self):
        print("\n-------------test_exportMP3------------\n")


 

if __name__ == "__main__":
    import os
    os.system("hrun C:\Users\ws\Desktop\login.yml")
    # suite = unittest.TestSuite()
    # for i in range(1,4):
    #     setattr(suite, 'test_case%d' % i, Action.generateTest(i))
    #
    #
    #
    # # suite = unittest.TestSuite()
    # # Test = ("test_exportVideo", "test_exportGif", "test_exportMP3")
    # # for i in Test:
    # #     print(i)
    # #     suite.addTest(Runner(i))
    # runner = unittest.TextTestRunner()
    # result = runner.run(suite)

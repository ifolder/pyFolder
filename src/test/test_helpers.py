#-*- coding: utf-8 -*-

import base64
import os
import shutil
import sys
import time
import unittest

sys.path.append ('../')

from pyFolder import *
from core.dbm import DBM
from core.config import ConfigManager

from suds import WebFault

from setup import Setup

IFOLDER_NAME = 'TestHelpers'
TEST_CONFIG = Setup ()

class TestHelpers (unittest.TestCase):

    def setUp (self):
        os.makedirs (TEST_CONFIG.USERDATA_A['prefix'])
        self.cm = ConfigManager (runfromtest=True, **TEST_CONFIG.USERDATA_A)
        self.pyFolder = pyFolder (self.cm, runfromtest=True)
        
    def tearDown (self):
        self.pyFolder.dbm = None
        shutil.rmtree (TEST_CONFIG.USERDATA_A['prefix'], True)

    def test_add_conflicted_suffix (self):
        aFile = '/lol\\foo/bar/baz/file.exe.lol'
        aDirectory = '/lol\\bar'
        Suffix = 'conflicted'

        self.assertEqual (\
            self.pyFolder.add_conflicted_suffix (aFile, Suffix), \
                '/lol\\foo/bar/baz/file.exe-{0}.lol'.format (Suffix))
        
        self.assertEqual (\
            self.pyFolder.add_conflicted_suffix (aDirectory, Suffix), \
                '/lol\\bar-{0}'.format (Suffix))
        
        aFile = '/lol/.bar'
        
        self.assertEqual (\
            self.pyFolder.add_conflicted_suffix (aFile, Suffix), \
                '/lol/.bar-{0}'.format (Suffix))
        
        aFile = '/lol/.bar.exe'
        
        self.assertEqual (\
            self.pyFolder.add_conflicted_suffix (aFile, Suffix), \
                '/lol/.bar-{0}.exe'.format (Suffix))
        
    def test_strip_invalid_characters (self):

        if sys.platform in [ 'win32', 'os2', 'os2emx' ]:
            return
        
        InvalidCharacters = [ '\\', ':', '*', '?', '\"', '<', '>', '|' ]
        Replacement = 'foo'
        InvalidPath = '/foo/bar/lol/{0}'
        ValidPath = InvalidPath.format (Replacement)
        
        for Char in InvalidCharacters:
            
            self.assertEqual (\
                self.pyFolder.strip_invalid_characters (\
                    InvalidPath.format (Char), Replacement), ValidPath)
        
if __name__ == '__main__':
    unittest.main ()
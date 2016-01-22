#!/usr/bin/env python2
# -*- coding: utf-8-*-
import unittest
import imp
from client import stt, jarvispath


def cmuclmtk_installed():
    try:
        imp.find_module('cmuclmtk')
    except ImportError:
        return False
    else:
        return True


def pocketsphinx_installed():
    try:
        imp.find_module('pocketsphinx')
    except ImportError:
        return False
    else:
        return True


@unittest.skipUnless(cmuclmtk_installed(), "CMUCLMTK not present")
@unittest.skipUnless(pocketsphinx_installed(), "Pocketsphinx not present")
class TestSTT(unittest.TestCase):

    def setUp(self):
        self.jarvis_clip = jarvispath.data('audio', 'jarvis.wav')
        self.time_clip = jarvispath.data('audio', 'time.wav')

        self.passive_stt_engine = stt.PocketSphinxSTT.get_passive_instance()
        self.active_stt_engine = stt.PocketSphinxSTT.get_active_instance()

    def testTranscribejarvis(self):
        """
        Does jarvis recognize his name (i.e., passive listen)?
        """
        with open(self.jarvis_clip, mode="rb") as f:
            transcription = self.passive_stt_engine.transcribe(f)
        self.assertIn("jarvis", transcription)

    def testTranscribe(self):
        """
        Does jarvis recognize 'time' (i.e., active listen)?
        """
        with open(self.time_clip, mode="rb") as f:
            transcription = self.active_stt_engine.transcribe(f)
        self.assertIn("TIME", transcription)

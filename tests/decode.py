"""
Tests for the decode() function.

Copyright 2020 Brave Software Inc.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""
import unittest

from simplepadding import decode


class SimplePaddingDecoding(unittest.TestCase):
    """Test the removal of various forms of padding."""

    def test_invalid_length(self):
        """Use an invalid length header."""
        with self.assertRaises(ValueError):
            decode(b'')
        with self.assertRaises(ValueError):
            decode(b'\xFF')
        with self.assertRaises(ValueError):
            decode(b'\x00\x00\x00')

    def test_file_too_small(self):
        """Use a file shorter than the length header."""
        with self.assertRaises(ValueError):
            decode(b'\x00\x00\x00\x01')
        with self.assertRaises(ValueError):
            decode(b'\x00\x00\x00\x04ABC')
        with self.assertRaises(ValueError):
            decode(b'\x00\x00\x00\x08ABCDPPP')

    def test_empty_payload(self):
        """Use an empty file."""
        self.assertEqual(
            decode(b'\x00\x00\x00\x00'),
            b''
        )

    def test_payload_without_padding(self):
        """Use a payload which isn't padded."""
        self.assertEqual(
            decode(b'\x00\x00\x00\x04ABCD'),
            b'ABCD'
        )
        self.assertEqual(
            decode(b'\x00\x00\x01\x00aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'),
            b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        )

    def test_payload_with_padding(self):
        """Use a payload which isn padded."""
        self.assertEqual(
            decode(b'\x00\x00\x00\x04ABCDPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP'),
            b'ABCD'
        )
        self.assertEqual(
            decode(b'\x00\x00\x00\x01PP'),
            b'P'
        )

"""
Tests for the encode() function.

Copyright 2020 Brave Software Inc.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""
import unittest

from simplepadding import encode


class SimplePaddingEncoding(unittest.TestCase):
    """Test various forms of padding."""

    def test_invalid_target_length(self):
        """Use values for the length target."""
        # Target length is smaller than the payload length.
        with self.assertRaises(ValueError):
            encode(b'ABCD', 2)

        # Target length doesn't account for the length header.
        with self.assertRaises(ValueError):
            encode(b'ABCD', 4)

        # Target length is larger than the limit.
        with self.assertRaises(ValueError):
            encode(b'ABCD', 4 * 1024 * 1024 * 1024 + 1)

    def test_endianness(self):
        """Use a payload that will be encoded differently in LE and BE arch."""
        self.assertEqual(
            encode(b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 255 + 4),
            b'\x00\x00\x00\xffaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        )
        self.assertEqual(
            encode(b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 256 + 4),
            b'\x00\x00\x01\x00aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        )

    def test_padding_not_needed(self):
        """Use a payload that doesn't need to be padded."""
        self.assertEqual(
            encode(b'ABCD', 8),
            b'\x00\x00\x00\x04ABCD'
        )

    def test_padding_empty_payload(self):
        """Use an empty payload."""
        self.assertEqual(
            encode(b'', 4),
            b'\x00\x00\x00\x00'
        )
        self.assertEqual(
            encode(b'', 10),
            b'\x00\x00\x00\x00PPPPPP'
        )

    def test_padding_needed(self):
        """Use a payload that needs to be padded."""
        self.assertEqual(
            encode(b'ABCD', 9),
            b'\x00\x00\x00\x04ABCDP'
        )

    def test_padding_utf8(self):
        """Use a UTF-8 payload."""
        self.assertEqual(
            encode(b'\x46\x72\x61\x6e\xc3\xa7\x6f\x69\x73', 15),
            b'\x00\x00\x00\x09Fran\xc3\xa7oisPP'
        )
        self.assertEqual(
            encode('François'.encode('utf-8'), 15),
            b'\x00\x00\x00\x09Fran\xc3\xa7oisPP'
        )

    def test_padding_binary(self):
        """Use a binary payload."""
        image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x03\x00\x00\x00(-\x0fS\x00\x00\x00\x99PLTE\xd73 \xb0(\x12\xf9=$y\x1c\x12\xba)\r\xe0.\x0b\x17\x06\x00\xf4/\t7\r\t\x7f\x1c\x11\xee:(\xdb3\x18\xdd0\x12\xf0:*\xfbB%\xee-\x00\xde0)\xf00\x0b\xf2;%\xe2+\x01\xff?&\xf0-\x00\xf9\xe2\xe1\xfc\x88v\xffU>\xff\xff\xff\xfc\xfa\xfc\xf7\xf5\xf7\xffB+\xf5\xf0\xf4\xfb\xb0\xa5\xf8\x96\x85\xf9\xa3\x97\xf2?\x17\xfeJ0\xf4\xc3\xbd\xf9jR\xff\xcc\xc6\xff\xd4\xce\xff\xf5\xf4\xf4\xd2\xcf\xfb\xeb\xec\xf1L(\xf89-\xf99\x1f\xf5-\x00\xfb/\x08\xf15\n\xfawb\xf1]=\xf83\'w\xb26\xb4\x00\x00\x00\x01tRNS\x00@\xe6\xd8f\x00\x00\x00\x85IDATx\xdam\x8cE\x02\xc2@\x0cE\x83\xbb\x8f\x85\xb4\x1d\xc3\x1d\xee\x7f7\xbc\xde\xb7\xfb\n\xd5\xccO\x1f\x12y|\xc4\xf4\xbf:`j\x1b-\xc9{\xc1\xf9\xd7\xa83\x14\x02)\xf4\xc2\xfc\x8c`\x83\x18I\xb2"\x0cy\xebk(D\xdc\xd0!\x0cw\xbf\xc6\x9c)\x94{\xb2a\xfc\x01\x8c!\xae\xc7ax\xc8\x1a\xd1%\x0c5_\xc4\x86s[\xd2\xf7\xb8\x00#\xc6\x14\x92\xe7\x89\x01\xec\x8d<s\xde\x81\x8cs9\x7fuL\xfdm@\x9e8~\x01\x14/\x0fe\xe56:\xd6\x00\x00\x00\x00IEND\xaeB`\x82'
        self.assertEqual(
            encode(image, 400),
            b'\x00\x00\x01\x70' + image + b'PPPPPPPPPPPPPPPPPPPPPPPPPPPP'
        )

        feed = b'\x1f\x8b\x08\x08\x7f\xfe\x98^\x02\x03feed.json\x00\xab\xe6R\x00\x02\xa5\xec\xd4J%+\x05\xa5\xb2\xc4\x9c\xd2T%\xaeZ.\x00%\x02\xf2\x8b\x17\x00\x00\x00'
        self.assertEqual(
            encode(feed, 75),
            b'\x00\x00\x00\x33' + feed + b'PPPPPPPPPPPPPPPPPPPP'
        )

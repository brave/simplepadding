"""
Module used to add and remove simple padding to binary files.

Copyright 2020 Brave Software Inc.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.
"""
import struct

MAX_LENGTH = 2**32  # 4 GB


def decode(data):
    """Extract a payload from its padding by reading its length header."""
    data_length_without_header = len(data) - 4
    if data_length_without_header < 0:
        raise ValueError('Data must be at least 4 bytes long', len(data))

    payload_length = struct.unpack('!L', data[0:4])[0]

    if data_length_without_header < payload_length:
        raise ValueError('Payload is shorter than the expected length',
                         data_length_without_header, payload_length)

    return data[4:4 + payload_length]


def encode(payload, target_length):
    """Pad a payload to a certain size, prefixing it with the original size."""
    no_padding_length = len(bytes(payload)) + 4
    if target_length < no_padding_length:
        raise ValueError('Payload without padding is larger than the target'
                         ' length', no_padding_length, target_length)

    if target_length > MAX_LENGTH:
        raise ValueError('Target length too large', target_length)

    length_header = struct.pack('!L', len(payload))

    padding_footer = b''
    while len(padding_footer) < (target_length - no_padding_length):
        padding_footer += b'P'

    return length_header + payload + padding_footer

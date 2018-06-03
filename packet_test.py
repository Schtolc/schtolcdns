import pytest
from packet import Packet


class TestPacket(object):
    def test_seek(self):
        packet = Packet()
        assert packet.position == 0

        packet.seek(10)
        assert packet.position == 10

        with pytest.raises(IndexError):
            packet.seek(513)

    def test_read(self):
        packet = Packet()
        assert packet.read_byte() == 0b0
        packet.seek(0)

        packet.buffer = b'\xC0\x0C\x00\x05'
        assert len(packet.buffer) == 4
        assert packet.read_byte() == 0b11000000
        assert packet.position == 1
        packet.seek(0)

        assert packet.read_uint16() == 49164
        assert packet.position == 2
        packet.seek(0)

        assert packet.read_uint32() == 3222011909
        assert packet.position == 4
        packet.seek(0)

        with pytest.raises(IndexError):
            packet.read_uint32()
            packet.read_uint32()

    def test_read_query_name(self):
        packet = Packet()

        packet.buffer = bytearray('\x06google\x03com\x00'.encode('UTF-8')) + bytearray([0xC0, 0x07])
        assert packet.read_query_name() == "google.com"
        assert packet.position == 12

        assert packet.read_query_name() == "com"
        assert packet.position == 14

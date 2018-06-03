from packet import Packet

packet = Packet()
print(len(packet.buffer))
packet.buffer[0] = 0b1
packet.buffer[1] = 0b1
packet.buffer[2] = 0b1
packet.buffer[3] = 0b1
print(packet.read_uint32())

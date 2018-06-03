class Packet:
    def __init__(self):
        self.buffer = bytearray(b'\x00' * 512)
        self.position = 0

    def seek(self, position):
        if position > len(self.buffer):
            raise IndexError('seek failed with position {}'.format(position))
        self.position = position

    def read_byte(self):
        self.seek(self.position + 1)
        return self.buffer[self.position - 1]

    def read_uint16(self):
        self.seek(self.position + 2)
        return int.from_bytes(self.buffer[self.position - 2:self.position], "big")

    def read_uint32(self):
        self.seek(self.position + 4)
        return int.from_bytes(self.buffer[self.position - 4:self.position], "big")

    def read_query_name(self):
        query_name = ""
        current_position = self.position
        jumped = False
        while True:
            label_length = self.buffer[current_position]
            if label_length & 0xC0 == 0xC0:
                if not jumped:
                    self.seek(current_position + 2)
                second_length_byte = self.buffer[current_position + 1]
                offset = (label_length ^ 0xC0) << 8 | second_length_byte
                current_position = offset
                jumped = True
            else:
                current_position += 1
                if label_length == 0:
                    break
                if len(query_name):
                    query_name = query_name + '.'
                query_name = \
                    query_name + self.buffer[current_position:current_position + label_length].decode('utf-8')
                current_position += label_length

        if not jumped:
            self.seek(current_position)

        return query_name

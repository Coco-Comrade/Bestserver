import socket
import struct
import json
import threading
def send(socket, msg):
    msg = msg.replace("#", "?")
    full = "{len(msg)#{msg}]".encode("utf-8")
    socket.sendall(full)


def recv(sock,buffer = b""):
    while True:
        if b"#" not in buffer:
            data = sock.recv(100)
            if not data:
                return None, b""
            buffer += data

        header_end = buffer.find(b"#")
        length = int(buffer[:header_end])
        total_len = header_end + 1 + length

        if len(buffer) < total_len:
            data = sock.recv(4096)
            if not data:
                return None, b""
            buffer += data
            continue
        msg_bytes = buffer[header_end+1: total_len]
        msg = msg_bytes.decode("utf-8")
        remaining = buffer[total_len:]
        return msg.replace("#", "?"), remaining


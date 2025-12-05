import logging
import socket
import struct
import json
import threading
def send(sock, msg):
    msg = msg.replace("#", "?")
    full = f"{len(msg)}#{msg}".encode("utf-8")
    sock.sendall(full)


def Send_Bin(sock,data):
    size = len(data)
    header = f"BINARY:{size}#".encode("utf-8")
    sock.sendall(header)
    sock.sendall(data)

def Recv_Bin(sock,size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            logging.error("recv failed")
            return None
        data += chunk
    return data


def recv(sock,buffer = b""):
    while True:
        if b"#" not in buffer:
            data = sock.recv(100)
            if not data:
                return None, b""
            buffer += data

        header_end = buffer.find(b"#")
        try:
            length = int(buffer[:header_end])
        except ValueError:
            return None, buffer
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



import socket as socket
import struct
import _thread as thread
import numpy as np
import ml_modules
import ml_collection as ml_col

# TODO take an arbitrary data format and arbitrary data matching that format and turn into bytes

DEFAULT_PORT = 12235
PORT = 12235
TIMEOUT = 3.0
BUF_SIZE = 4096
FLOAT_BYTES = 4

HOST = socket.gethostbyname(socket.gethostname())

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

# Data is formatted such that each row is one sample
def execute(func_id, data, args):
    # print("Received data: ", data)
    algo_class = ml_col.algorithms[func_id]
    algo_instance = algo_class(data, args)
    res = algo_instance.run()
    print("Result: ", res)
    
    pass

def parse_next_arg(msg):
    arg_name_len = int.from_bytes(msg[0:4], "big")
    if arg_name_len == 0:
        return None
    arg_name = msg[4:arg_name_len+4].decode("utf-8")
    
    # TODO allow the value to be a float
    value = int.from_bytes(msg[4+arg_name_len:4+arg_name_len+4], "big")

    bytes_parsed = 4 + arg_name_len + 4
    return arg_name, value, bytes_parsed


def handle_connection(client_socket, client_addr):
    print("Accepted TCP Connection from ", client_addr)
    client_socket.settimeout(TIMEOUT)
    # TODO change endianness stuff maybe
    msg = client_socket.recv(BUF_SIZE)

    msg_len = int.from_bytes(msg[0:4], "big")
    func_id = int.from_bytes(msg[4:8], "big")
    # number of floats per sample
    sample_dims = 1

    bytes_received = len(msg)
    while bytes_received < msg_len:
        # TODO stream data to avoid heavy memory usage
        msg += client_socket.recv(BUF_SIZE)
        bytes_received = len(msg)

    args = {}
    
    msg = msg[8:]

    res = parse_next_arg(msg)
    while res is not None:
        arg_name, value, bytes_parsed = res
        args[arg_name] = value

        msg = msg[bytes_parsed:]
        res = parse_next_arg(msg)
        pass
    msg = msg[4:]

    # while bytes_received < msg_len:
    #     msg = client_socket.recv(BUF_SIZE)
        # TODO catch corner case where a string is not aligned

    if "dims" in args:
        sample_dims = int(args["dims"])
    
    bytes_per_struct = FLOAT_BYTES * sample_dims
    data = np.frombuffer(msg, dtype=">f4")
    num_samples = int(len(data) / sample_dims)
    new_shape = (num_samples, sample_dims)

    data = np.reshape(data, new_shape)

    res = execute(func_id, data, args)

    client_socket.close()


while True:
    (client_socket, addr) = server_socket.accept()
    thread.start_new_thread(handle_connection, (client_socket, addr))

server_socket.close()


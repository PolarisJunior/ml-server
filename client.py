import socket as socket
import _thread as thread
import struct

SERVER_PORT = 12235
CLIENT_PORT = 11111
TIMEOUT = 3.0

HOST = socket.gethostbyname(socket.gethostname())
# HOST = "localhost"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# client_socket.bind((HOST, CLIENT_PORT))
client_socket.connect((HOST, SERVER_PORT))
# client_socket.sendto((63).to_bytes(4, byteorder="big"), (HOST, SERVER_PORT))
print("connected")
msg_len = 8
func_id = 1

def args_to_bytes(args):
    res = b''
    for arg_name in args:
        arg_value = args[arg_name]
        arg_name_encoded = arg_name.encode("utf-8")
        arg_name_len = len(arg_name_encoded)

        res += arg_name_len.to_bytes(4, "big")
        res += arg_name_encoded
        res += arg_value.to_bytes(4, "big")

    return res

samples = [5.163, 32.93, 13.93, 42.0, 11.2, 13.5]
sample_bytes = struct.pack(">" + str(len(samples))+"f", *(samples))
separator = (0).to_bytes(4, "big")

args = { "k": 4, "n": 200, "dims": 3}
args_bytes = args_to_bytes(args)
payload = func_id.to_bytes(4, "big") + args_bytes + separator + sample_bytes
msg_len = len(payload) + 4

msg = msg_len.to_bytes(4, "big") + payload

client_socket.send(msg)
client_socket.close()

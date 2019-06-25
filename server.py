
import socket as socket
import _thread as thread

# TODO take an arbitrary data format and arbitrary data matching that format and turn into bytes

PORT = 12235
TIMEOUT = 3.0
BUF_SIZE = 4096

HOST = socket.gethostbyname(socket.gethostname())

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

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

    msg = client_socket.recv(BUF_SIZE)
    print(msg)

    msg_len = int.from_bytes(msg[0:4], "big")
    func_id = int.from_bytes(msg[4:8], "big")

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

    # while bytes_received < msg_len:
    #     msg = client_socket.recv(BUF_SIZE)
        # TODO catch corner case where a string is not aligned
    print(msg_len, func_id, bytes_received)
    for k in args:
        print(k, args[k])

    client_socket.settimeout(TIMEOUT)
    client_socket.close()
    pass

while True:
    (client_socket, addr) = server_socket.accept()
    thread.start_new_thread(handle_connection, (client_socket, addr))

server_socket.close()

# foo = "foobar".encode('utf-8')
# print(foo[0:4])




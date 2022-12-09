from socket import *
import threading

worker_address = ['192.171.20.114', '192.171.20.115', '192.171.20.118', '192.171.20.119', '192.171.20.120']
SERVER_IP = '192.171.20.113'
SERVER_PORT = 2048
WORKER_PORT = 2000
responses = []


# def comm_worker(worker_no, msg, cnt):
#     with socket(AF_INET, SOCK_STREAM) as s:
#         s.connect((worker_address[worker_no - 1], WORKER_PORT))
#         s.sendall(msg.encode())
#         data = s.recv(1024)
#         responses[worker_no - 1] = data.decode()
#         if cnt > 1 and (worker_no == 1 and data or worker_no != 1):
#             comm_worker(worker_no + 1, msg, cnt - 1)

def worker_thread(conn, data, idx):
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((worker_address[idx], WORKER_PORT))
        s.sendall(data)
        response = s.recv(1024).decode()
        print(response)
        conn.sendall(response.encode())


with socket(AF_INET, SOCK_STREAM) as s:
    s.bind((SERVER_IP, SERVER_PORT))
    while True:
        s.listen()
        conn, addr = s.accept()
        print(f"Connected to {addr}")
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode()
                num_worker = int(message.split(' ')[0])
                hash_str = message.split(' ')[1]
                print(num_worker)
                print(hash_str)
                # cnt = 0
                # comm_worker(1, hash_str, num_worker)
                for i in range(num_worker):
                    t = threading.Thread(target=worker_thread, args=(conn, hash_str.encode(), i))
                    t.start()
                    t.join()

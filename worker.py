from socket import *
import hashlib
import itertools
import argparse

WORKER = ['192.171.20.114', '192.171.20.115', '192.171.20.118', '192.171.20.119', '192.171.20.120']
PORT = 2000
SERVER_IP = '192.171.20.113'
SERVER_PORT = 2048
samples = ['IKCVGEswxSfRTgyuaJlPvbHAMrzYOnQUNBZXcWDtFhqemoLjpikd',
           'jmnfkOzMSbeTKBIQgwRpNUZvdGYsHaoiyLrVxCXEAqJlhtFDWcPu',
           'hAEXJLgtUezDCVvHoSkMOPFKsdrYZWxmRGajpByQcuiTfqnlwINb',
           'oKTBlmrGXIMzvpSsPCUAtxjHNLDuWcdiyYfnwQEZORJFkaqghVbe',
           'JFsbQYOWfZHgnTvkephGAumcjxEdzIRqoSywVlDPrBUaMCitKNXL']

parser = argparse.ArgumentParser()
parser.add_argument('WORKER_NO', type=int, help='worker serial number')
args = parser.parse_args()

with socket(AF_INET, SOCK_STREAM) as s:
    s.bind((WORKER[args.WORKER_NO-1], PORT))
    print(f"worker {args.WORKER_NO} ready")
    while True:
        s.listen()
        conn, addr = s.accept()
        print(f"Connected to {addr}")
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                hash_str = data.decode()
                print(hash_str)

                for comb in itertools.product(samples[args.WORKER_NO-1], repeat=5):
                    pwd = ''.join(comb)
                    md5 = hashlib.md5()
                    md5.update(pwd.encode('utf-8'))
                    pwd_hash = md5.hexdigest()
                    if pwd_hash == hash_str:
                        break

                conn.sendall(pwd.encode())
                print("cracked " + pwd)

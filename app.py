from flask import Flask, render_template, request, redirect, url_for
from socket import *
import hashlib
import time

# regard as failure if using more than 30 seconds
TIMEOUT = 30

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/index', methods=['POST', 'GET'])
def web_interface():
    if request.method == 'POST':
        pwd = request.form['password']
        num_worker = request.form['num_worker']
        fail = False
        # return redirect(url_for("success", pwd=pwd, num_worker=num_worker))

        with socket(AF_INET, SOCK_STREAM) as s:
            HOST = '192.171.20.113'
            PORT = 2048
            s.connect((HOST, PORT))
            md5 = hashlib.md5()
            md5.update(pwd.encode('utf-8'))
            msg = str(num_worker) + ' ' + md5.hexdigest()
            start = time.time()
            s.sendall(msg.encode())
            print(msg)
            data = s.recv(1024)
            # while True:
            #     data = s.recv(1024)
            #     if not data:
            #         break
            #     # current = time.time()
            #     # if current - start > TIMEOUT:
            #     #     fail = True
            #     #     break
            end = time.time()
            s.close()

        if fail:
            return redirect(url_for("failure"))
        else:
            cracked = data.decode()
            time_interval = (end - start) * 1000
            return redirect(url_for("success", pwd=cracked, num_worker=num_worker, cost_time=time_interval))


@app.route('/success/<pwd>/<num_worker>/<cost_time>')
def success(pwd, num_worker, cost_time):
    return f'Cracked successfully using {num_worker} workers after {cost_time} ms. Your password is' \
           f': {pwd}.'


@app.route('/failure')
def failure():
    return "Used more then expected time. Failed to crack password."


if __name__ == '__main__':
    app.run()

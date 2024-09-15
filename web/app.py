from Crypto.Hash import SHA256
from flask import Flask, request, render_template, redirect, url_for
from subprocess import Popen, PIPE
import re

app = Flask(__name__, template_folder='./templates')

USERS = {
	'admin': {
		'password': SHA256.new(b'admin').hexdigest(),
	}
}

def get_mac_address(ip):
	p = Popen(['arp', '-n', ip], stdout=PIPE)
	output = p.communicate()[0].decode()
	mac = re.search(r'(([a-f\d]{1,2}:){5}[a-f\d]{1,2})', output)
	if mac:
		return mac.group(0)
	else:
		return None

def add_to_iptables(mac):
	Popen(['iptables', '-A', 'AUTHORIZED', '-m', 'mac', '--mac-source', mac, '-j', 'ACCEPT'])
	Popen(['iptables', '-t', 'nat', '-A', 'AUTHORIZED', '-m', 'mac', '--mac-source', mac, '-j', 'ACCEPT'])

def authorize(ip):
	mac = get_mac_address(ip)
	if mac:
		add_to_iptables(mac)

@app.route('/api/login', methods=['POST'])
def login():
	username = request.form['username']

	if username not in USERS:
		return redirect(url_for('login_failed'))

	password = request.form['password']
	password_hash = SHA256.new(password.encode()).hexdigest()
	if password_hash == USERS[username]['password']:
		authorize(request.remote_addr)
		return '登入成功'
	else:
		return redirect(url_for('login_failed'))

@app.route('/login_failed')
def login_failed():
	return render_template('login_failed.html')

@app.route('/')
@app.route('/generate_204')
def index():
	return render_template('index.html')
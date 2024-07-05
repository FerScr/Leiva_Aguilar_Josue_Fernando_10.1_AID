from flask import Flask, request, render_template, redirect, url_for
import os
import subprocess

app = Flask(__name__)
PLAYBOOK_DIR = '/app/playbooks'
INVENTORY_FILE = '/app/inventory'

@app.route('/')
def index():
    playbooks = os.listdir(PLAYBOOK_DIR)
    output = request.args.get('output', '')
    return render_template('index.html', playbooks=playbooks, output=output)

@app.route('/run_playbook', methods=['POST'])
def run_playbook():
    playbook = request.form['playbook']
    playbook_path = os.path.join(PLAYBOOK_DIR, playbook)
    result = os.popen(f'ansible-playbook -i {INVENTORY_FILE} {playbook_path}').read()
    return redirect(url_for('index', output=result))

@app.route('/playbook_factory')
def playbook_factory():
    playbooks = os.listdir(PLAYBOOK_DIR)
    return render_template('playbook_factory.html', playbooks=playbooks)

@app.route('/get_playbook_content')
def get_playbook_content():
    playbook = request.args.get('playbook')
    playbook_path = os.path.join(PLAYBOOK_DIR, playbook)
    with open(playbook_path, 'r') as file:
        content = file.read()
    return content

@app.route('/save_playbook', methods=['POST'])
def save_playbook():
    playbook = request.form['playbook']
    playbook_content = request.form['playbookContent']
    new_playbook_name = request.form.get('newPlaybookName', '').strip()

    if playbook == 'new':
        if not new_playbook_name:
            return "El nombre del nuevo playbook no puede estar vacío", 400
        playbook_name = new_playbook_name + '.yml'
    else:
        playbook_name = playbook

    playbook_path = os.path.join(PLAYBOOK_DIR, playbook_name)
    with open(playbook_path, 'w') as file:
        file.write(playbook_content)
    return redirect(url_for('playbook_factory'))

@app.route('/add_host', methods=['POST'])
def add_host():
    hostname = request.form['hostname']
    hostip = request.form['hostip']

    # Agregar al archivo de inventario
    with open(INVENTORY_FILE, 'a') as file:
        file.write(f'{hostname} ansible_host={hostip}\n')

    # Compartir la clave SSH al nuevo host
    ssh_command = f'ssh-copy-id -i /root/.ssh/id_rsa.pub {hostname}@{hostip}'
    subprocess.run(ssh_command, shell=True, check=True)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

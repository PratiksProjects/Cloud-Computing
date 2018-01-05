import requests
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/metadata')
def get_data():
    my_list = {}
    my_list['instance-id'] = requests.get('http://169.254.169.254/latest/meta-data/instance-id').content
    my_list['ami-launch-index'] = requests.get('http://169.254.169.254/latest/meta-data/ami-launch-index').content
    my_list['public-hostname'] = requests.get('http://169.254.169.254/latest/meta-data/public-hostname').content
    my_list['public-ipv4'] = requests.get('http://169.254.169.254/latest/meta-data/public-ipv4').content
    my_list['local-hostname'] = requests.get('http://169.254.169.254/latest/meta-data/local-hostname').content
    my_list['local-ipv4'] = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4').content
    return render_template('index.html',my_list = my_list)
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

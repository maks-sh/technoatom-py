import requests
import configparser

conf = configparser.RawConfigParser()
conf.read('config.conf')

if __name__ == '__main__':
    for i in range(5):
        response = requests.get('http://' + conf.get('params', 'url') + ':' + conf.get('params', 'port') + '/')
        print('status: %d' % response.status_code)
        print('content: %s' % response.text)

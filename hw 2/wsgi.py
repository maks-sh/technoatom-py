from random import randint
from time import sleep
from wsgiref.simple_server import make_server
import configparser

conf = configparser.RawConfigParser()
conf.read('config.conf')

def events(max_delay, limit):
    while True:
        delay = randint(1, max_delay)
        print(delay)
        if delay >= limit:
            sleep(limit)
            yield None
        else:
            sleep(delay)
            yield 'Event generated, awaiting %d s' % delay

generator = events(15, 10)

class SimpleWSGIApplication(object):

    def __init__(self, environment, start_response):
        print('Get request')
        self.environment = environment
        self.start_response = start_response
        self.headers = [
            ('Content-type', 'text/plain; charset=utf-8')
        ]

    def __iter__(self):
        print('Wait for response')
        if self.environment.get('PATH_INFO', '/') == '/':
            event = next(generator)
            print(event)
            if event is None:
                yield from self.ok_response_but_no_content('No content')
            else:
                yield from self.ok_response(event)
        else:
            self.not_found_response()
        print('Done')

    def not_found_response(self):
        print('Create response')
        print('Send headers')
        self.start_response('404 Not Found', self.headers)
        print('Headers is sent')
        yield ('404 error').encode('utf-8')

    def ok_response(self, message):
        print('Create response')
        print('Send headers')
        self.start_response('200 OK', self.headers)
        print('Headers is sent')
        print('Send body')
        yield ('%s\n' % message).encode('utf-8')
        print('Body is sent')

    def ok_response_but_no_content(self, message):
        print('Create response')
        print('Send headers')
        self.start_response('204 No Content', [])
        print('Status is sent')
        yield ('%s\n' % message).encode('utf-8')

if __name__ == '__main__':
    server = make_server(conf.get('params', 'url'), int(conf.get('params', 'port')), SimpleWSGIApplication)
    server.serve_forever()

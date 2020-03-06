from http.server import  SimpleHTTPRequestHandler
from io import BytesIO

class MyHandler(SimpleHTTPRequestHandler):

    '''
    def __init__(self, stat_dict, seongnam_track_list, around_track_list):
        self.stat_dict = stat_dict
        self.seongnam_track_list = seongnam_track_list
        self.around_tack_list = around_track_list
    '''

    def do_GET(self):
        print(self.path)
        if not self.path.startswith("/v1/sn_corona"):
            self.send_response(502)
            self.end_headers()
            return
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, world!                       asdfasdf')

'''
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

'''
from http.server import  SimpleHTTPRequestHandler
from io import BytesIO
import json

class MyHandler(SimpleHTTPRequestHandler):

    def do_POST(self):
        if self.headers['Authorization'] != '12034u8014u8r2ejd8123j1423412341adf1':
            self.send_response(502)
            self.end_headers()
            return
        if self.path == "/v1/sn_corona/sn_stats":
            self.__response_sn_stats()
            return
        elif self.path == "/v1/sn_corona/hp1_patients":
            pass
        elif self.path == "/v1/sn_corona/ch1_patients":
            pass
        elif self.path == "/v1/sn_corona/ar_patients":
            pass
        else:
            self.send_response(502)
            self.end_headers()
            return

    def __response_sn_stats(self):
        fr = open('data/sn_stats.txt', 'r')
        data = fr.read()
        data = "성남시 코로나 현황\n"+data

        fr.close()
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        str_json = {
            "version": "2.0",
            "template":{
                "outputs":[
                    {
                        "simpleText": {
                            "text":str(data)
                        }
                    }
                ]
            }
        }
        self.wfile.write(bytes(json.dumps(str_json), "utf-8"))

    def __response_sn_patients(self):
        pass
    def __response_ar_patients(self):
        pass

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
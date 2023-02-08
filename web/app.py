import json
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = 'localhost'
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        result_string = "{'result': 'Hello, World wide web!'}"

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(result_string, 'utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        data_from_request = json.loads(post_data)
        print(data_from_request)

        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes('{"result": "ok", "data_status": "printed"}', 'utf-8'))


if __name__ == '__main__':
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print('Server started http://%s:%s' % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print('Server stopped')

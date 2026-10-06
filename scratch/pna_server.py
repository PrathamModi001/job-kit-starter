from http.server import HTTPServer, SimpleHTTPRequestHandler
import functools
import os

class PNAHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

if __name__ == '__main__':
    port = 8765
    scratch_dir = os.path.abspath('E:/Extra/job-kit-starter/scratch')
    handler = functools.partial(PNAHandler, directory=scratch_dir)
    server = HTTPServer(('127.0.0.1', port), handler)
    print(f'Server running on port {port} serving {scratch_dir}')
    server.serve_forever()

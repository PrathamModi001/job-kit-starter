from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

PDF_PATH = r"E:\Extra\job-kit-starter\job-kit-starter\output\Pratham_Modi_Base_Resume.pdf"

with open(PDF_PATH, "rb") as f:
    pdf_bytes = f.read()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(pdf_bytes)))
        self.end_headers()
        self.wfile.write(pdf_bytes)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

server = HTTPServer(("127.0.0.1", 8765), Handler)
print("Server running on http://127.0.0.1:8765/resume.pdf", flush=True)
server.serve_forever()

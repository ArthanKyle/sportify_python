from http.server import HTTPServer
from app import app
import os

port = int(os.environ.get('PORT', 3000))

if __name__ == '__main__':
    server_address = ('', port)
    httpd = HTTPServer(server_address, app)
    print(f"Server up and running on PORT: {port}")
    httpd.serve_forever()

# Matthew Garcia
# This is a basic test server that run locally on your machine.
import urllib
from GaikiParser import GaikiParser
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
HOST_NAME = "http://127.0.0.1:8000" # localhost
PORT_NUMBER = 8000  # 80 is default http



class Server(BaseHTTPRequestHandler):
    g_parser = GaikiParser("http://www.gaikai.com/careers")
    def do_GET(self):
       
        headers = { 'application/json', 'text/plain'}
        self.send_response(200)
        self.send_header('application/json', 'text/plain')
        self.end_headers()
        try:
            self.wfile.write(self.g_parser.getRequest(self.path))
        except IOError,e:
            if e.errno == errno.EPIPE:
                print "Client has closed the socket"
def main():
    
        httpd = HTTPServer(('', 8000), Server)
        print "Starting server"
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        print "Closing Server"
if __name__ == '__main__':
    main()


































import SocketServer
import re
import os.path
# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright  2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    okResponseHeader = "HTTP/1.1 200 OK"
    badRequestResponse = "HTTP/1.1 400 Bad Request\nContent-Length:145\nContent-Type:text/html;\n\n<!DOCTYPE html>\n<html><head><title>Bad Request</title></head><body><h1>400: Bad Request</h1>This server only supports GET requests.</body></html>"
    notFoundResponse = "HTTP/1.1 404 Not Found\nContent-Length:154\nContent-Type:text/html;\n\n<!DOCTYPE html>\n<html><head><title>Page Not Found</title></head><body><h1>404: Page Not Found</h1>The page you requested could not be found.</body></html>"
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        headers = self.data.split("\n")
        request = headers[0].split(" ")
        if(request[0] == "GET"):
            print ("{"+request[1]+"}")
            response = self.handleGet(request[1])
        else:
            self.request.sendall(self.badRequestResponse)
            return
        
        if(response is None):
            self.request.sendall(self.notFoundResponse)
            return
        
        self.request.sendall(response)
        
        
    def handleGet(self,requestedFile):
        requestedFile = "www" + requestedFile
        if(re.match('.*\/$', requestedFile)):
            requestedFile += "index.html"
            
        if(os.path.isfile(requestedFile)):
            contentFile = open(requestedFile, 'r')
            content = contentFile.read()
            contentFile.close()
        else:
            return None
        
        contentLength = len(content)
        response = self.okResponseHeader
        response += "\nContent-Length: " + str(contentLength)
        if(re.match('.*\.htm(l)?$',requestedFile)):
            response += "\nContent-Type: text/html"
        elif(re.match('.*\.css$',requestedFile)):
            response += "\nContent-Type: text/css"
        else:
            return None
        
        response += "\n\n" + content
        
        return response
        
    def sendReply(self, header, body):
        contentLength = len(body)
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

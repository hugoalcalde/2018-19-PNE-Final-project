"""This is the code of the server of the final practice"""
import http.server
import http.client
import socketserver
import termcolor
import json

PORT = 8000 # this is the port used in this practice.
METHOD = "GET"
HOSTNAME = "rest.ensembl.org"

headers = {'User-Agent' : 'http-client'}

class TestHandler(http.server.BaseHTTPRequestHandler): #this is the class of our server that derives from the protocol

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        # -- Parser the path
        list_resource = self.path.split('?')
        resource = list_resource[0]

        if resource == "/":
            f = open("index.html", 'r')
            code = 200
            # Read the file
            contents = f.read()

            content_type = 'text/html'

        elif resource == "/listSpecies":
            ENDPOINT = "/info/species?"
            conn = http.client.HTTPSConnection(HOSTNAME)
            conn.request(METHOD, ENDPOINT, None, headers)

            r1 = conn.getresponse()

            print(r1.status, r1.reason)
            text_json = r1.read().decode("utf-8")
            conn.close()

            info = json.loads(text_json)
            limit = 50
            species = ""
            counter = 0
            for element in info :
                species =  "\n" + species + element["name"]
                counter += 1
            f = open("limit.html", "w")
            f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>LIST OF SPECIES IN THE BROWSER</title>
</head>
<body>
   The number of species is : {}
   The name of the species is : {}
</body>
</html>'''.format(counter, species))


            f = open("limit.html", 'r')
            code = 200
            # Read the file
            contents = f.read()
            content_type = 'application/json'
        else:
            f = open("error.html", 'r')
            code = 404
            # Read the file
            contents = f.read()
            content_type = 'text/html'

        # Generating the response message
        self.send_response(code)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(str.encode(contents)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()

print("")
print("Server Stopped")
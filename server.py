"""This is the code of the server of the final practice"""

# first we get the information that we are going to need from the browser, working as a client
import http.server
import termcolor
import socketserver
import requests
PORT = 8000 # this is the port used in this practice.
socketserver.TCPServer.allow_reuse_address = True
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

            server = "http://rest.ensembl.org"
            ext = "/info/species?"

            r = requests.get(server + ext, headers={"Content-Type": "application/json"})


            decoded = r.json()
            species = "" #having a string is more useful when creating the html file in the program
            counter_species = len(decoded["species"])
            for element in decoded["species"]:
                species = species + element["display_name"]
                species = species + "<br>"
            f = open("limit.html", "w")
            f.write('''<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>LIST OF SPECIES IN THE BROWSER</title>
            </head>
            <body>
               The number of species is : {} <br>
               The names of the species are : {}
            </body>
            </html>'''.format(len(decoded["species"]), species))

            # Read the file
            f = open("limit.html", 'r')
            code = 200
            # Read the file
            contents = f.read()
            content_type = 'text/html'
        elif resource == "/karyotype" :
            species_selected = "homo_sapiens" #this is an example, then this should be taken from the index
            server = "http://rest.ensembl.org"
            ext = "/info/assembly/"

            r = requests.get(server + ext + species_selected + "?" , headers={"Content-Type": "application/json"})

            decoded = r.json()
            karyotype = ""
            for element in decoded["karyotype"] :
                karyotype = karyotype + "<br>" + element
            f = open("karyotype.html", "w")
            f.write('''<!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <title>KARYOTYPE OF A SPECIFIC SPECIES</title>
                        </head>
                        <body>
                           The names of the chromosomes are : {}
                        </body>
                        </html>'''.format(karyotype))

            # Read the file
            f = open("karyotype.html", 'r')
            code = 200
            # Read the file
            contents = f.read()
            content_type = 'text/html'
        elif resource == "/chromosomeLength" :
            chromo = "X" #preguntar si esto es un parámetro que indica el usuario o no y cambiarlo segun el index.html
            species_selected = "homo_sapiens" #CAMBIAR
            server = "http://rest.ensembl.org"
            ext = "/info/assembly/"

            r = requests.get(server + ext + species_selected + "?", headers={"Content-Type": "application/json"})

            decoded = r.json()
            for element in decoded["top_level_region"] :
                print(element["name"])
                if element["name"] == chromo:
                    length_chromosome = element["length"]
            f = open("length.html", "w")
            f.write('''<!DOCTYPE html>
                                    <html lang="en">
                                    <head>
                                        <meta charset="UTF-8">
                                        <title>LENGTH OF THE SELECTED CHROMOSOME</title>
                                    </head>
                                    <body>
                                       The length of the chromosome is :  {}
                                    </body>
                                    </html>'''.format(length_chromosome))

            # Read the file
            f = open("length.html", 'r')
            code = 200
            # Read the file
            contents = f.read()
            content_type = 'text/html'



        else :
            code = 0
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


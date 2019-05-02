import http.client

PORT = 8000
SERVER = 'localhost'

print("\nConnecting to server: {}:{}\n".format(SERVER, PORT))

# Connect with the server
conn = http.client.HTTPConnection(SERVER, PORT)

request_list = ["listSpecies?limit=45" , "listSpecies?" , "listSpecies?limit=as" , "karyotype?specie=human" , "karyotype?specie=mouse" , "chromosomeLength?specie=human&chromo=X" , "chromosomeLength?specie=mouse&chromo=X", "geneSeq?gene=FRAT1" , "geneSeq?gene=FRAT1", "geneInfo?gene=FRAT1" , "geneInfo?gene=FRAT2" , "geneCalc?gene=FRAT1" , "geneCalc?gene=FRAT2" , "geneList?chromo=X&start=0&end=300000", "geneList?chromo=X&start=0&end=1" ]
counter = 1
for request in request_list :
    conn.request("GET", "/" + request + "&json=1")

    # -- Read the response message from the server
    r1 = conn.getresponse()


    # -- Read the response's body
    data1 = r1.read().decode("utf-8")
    print(counter)
    counter +=1

    # -- Print the received data
    print(data1)
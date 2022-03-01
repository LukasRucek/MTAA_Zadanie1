# Zadanie č.1 z predmetu Mobilné technológie a aplikácie
# Vypracoval: Lukáš Rucek
# Použité sipfullproxy.py z githubu:https://github.com/tirfil/PySipFullProxy

import sipfullproxy
import socketserver
import socket
import sys
import time
import logging


# Funkcia slúži na úpravu SIP stavových kódov.
def translate(code):
    help_code = code.split(" ")
    if help_code[1] == "400":
        help_code[2] = "Zly Request"
    elif help_code[1] == "406":
        help_code[2] = "Neprijatie"
    elif help_code[1] == "408":
        help_code[2] = "Nedostupny"
    elif help_code[1] == "486":
        help_code[2] = "Obsadene"
        help_code[3] = ""
    elif help_code[1] == "487":
        help_code[2] = "Ziadost"
        help_code[3] = "Zrusena"
    elif help_code[1] == "603":
        help_code[2] = "Odmietnutie"
    elif help_code[1] == "100":
        help_code[2] = "Skusanie"
    elif help_code[1] == "180":
        help_code[2] = "Zvonenie"

    print(help_code)
    help_code = " ".join(help_code)

    return help_code


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', filename='proxy.log', level=logging.INFO,
                        datefmt='%H:%M:%S')
    logging.info(time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime()))
    hostname = socket.gethostname()
    logging.info(hostname)
    ipaddress = socket.gethostbyname(hostname)
    print(ipaddress)
    if ipaddress == "127.0.0.1":
        ipaddress = sys.argv[1]
    logging.info(ipaddress)
    sipfullproxy.recordroute = "Record-Route: <sip:%s:%d;lr>\n" % (ipaddress, sipfullproxy.PORT)

    sipfullproxy.topvia = "Via: SIP/2.0/UDP %s:%d" % (ipaddress, sipfullproxy.PORT)
    server = socketserver.UDPServer((ipaddress, sipfullproxy.PORT), sipfullproxy.UDPHandler)
    server.serve_forever()
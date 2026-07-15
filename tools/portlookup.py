import socket
from concurrent.futures import ThreadPoolExecutor

class portlookup:

    def __init__(self,domain):
        self.host = domain
    
    def port_scan(self, port):

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

                sock.settimeout(0.5)
                result = sock.connect_ex((self.host, port))

            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except OSError:
                    service = "unknown"

                return {
                    "port": port,
                    "state": "open",
                    "service": service
                }
            
        except Exception:
            return None

    def scan(self):
        OpenPort=[]

        with ThreadPoolExecutor(max_workers = 100) as executor:
            result =executor.map(self.port_scan, range(1,65536))
        
        for port in result:
            if port:
                OpenPort.append(port)

        return OpenPort

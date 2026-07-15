import socket
from concurrent.futures import ThreadPoolExecutor


class PortLookup:


    def __init__(self, domain):

        self.host = domain


    def port_scan(self, port):

        try:

            with socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            ) as sock:

                sock.settimeout(0.5)

                result = sock.connect_ex(
                    (self.host, port)
                )


            if result == 0:

                try:

                    service = socket.getservbyport(
                        port
                    )

                except OSError:

                    service = "unknown"


                return {
                    "port": port,
                    "protocol": "TCP",
                    "state": "open",
                    "service": service
                }


        except Exception:

            pass


        return None



    def scan(self):

        open_ports = []


        with ThreadPoolExecutor(
            max_workers=100
        ) as executor:


            results = executor.map(
                self.port_scan,
                range(1, 65536)
            )


        for result in results:

            if result:

                open_ports.append(result)



        return {
            "scanner": "PortLookup",
            "target": self.host,
            "status": "success",
            "data": {
                "total_open_ports": len(open_ports),
                "open_ports": open_ports
            }
        }
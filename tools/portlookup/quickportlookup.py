import socket
from concurrent.futures import ThreadPoolExecutor


class QuickPortLookup:


    ports = [20,21,22,23,25,53,80,110,139,143,443,445,465,587,993,995,1433,1521,3306,3389,5432,5900,6379,8080,8443

    ]


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
                    (
                        self.host,
                        port
                    )
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
                self.ports
            )



        for result in results:


            if result:

                open_ports.append(
                    result
                )



        return {


            "scanner": "QuickPortLookup",

            "target": self.host,

            "status": "success",


            "data": {


                "total_checked_ports": len(self.ports),


                "total_open_ports": len(open_ports),


                "open_ports": open_ports


            }

        }
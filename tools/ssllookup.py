import ssl
import socket
from datetime import datetime

class ssltool:

    def __init__(self,domain):
        self.host=domain
        self.port=443
    
    def scan(self):
        result={}

        try:
            configobj=ssl.create_default_context()

            with socket.create_connection((self.host, self.port),timeout=5) as sock:
                with configobj.wrap_socket(sock, server_hostname=self.host) as ssock:

                    license=ssock.getpeercert()

                    result["TLS Version"]=ssock.version()
                    result["Cipher"]=ssock.cipher()
                    result["Issuer"]=dict(i[0] for i in license["issuer"])
                    result["Subject"]=dict(i[0] for i in license["subject"])
                    result["Valid From"]=license("notBefore")
                    result["Valid Until"]=license("notAfter")

                    expire = datetime.strptime(license["notAfter"],"%b %d %H:%M:%S %Y %Z")

                    result["Days Remaining"]=(expire-datetime.utcnow()).days


        except Exception as e:
            result["error"]=str(e)
        
        return result
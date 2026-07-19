import ssl
import socket
from datetime import datetime


class SSLLookup:


    def __init__(self, domain):

        self.host = domain
        self.port = 443


    def parse_cert_field(self, field):

        return {
            key: value
            for item in field
            for key, value in item
        }


    def scan(self):

        result = {}


        try:

            context = ssl.create_default_context()


            with socket.create_connection(
                (self.host, self.port),
                timeout=5
            ) as sock:


                with context.wrap_socket(
                    sock,
                    server_hostname=self.host
                ) as ssock:


                    certificate = ssock.getpeercert()


                    result["tls_version"] = (
                        ssock.version()
                    )


                    result["cipher"] = (
                        ssock.cipher()
                    )


                    result["issuer"] = (
                        self.parse_cert_field(
                            certificate["issuer"]
                        )
                    )


                    result["subject"] = (
                        self.parse_cert_field(
                            certificate["subject"]
                        )
                    )


                    result["valid_from"] = (
                        certificate["notBefore"]
                    )


                    result["valid_until"] = (
                        certificate["notAfter"]
                    )


                    expire = datetime.strptime(
                        certificate["notAfter"],
                        "%b %d %H:%M:%S %Y %Z"
                    )


                    result["days_remaining"] = (
                        expire - datetime.utcnow()
                    ).days



                    if result["days_remaining"] < 0:

                        result["certificate_status"] = "certificate expired"

                    else:

                        result["certificate_status"] = "certificate valid"



                    # Security checks

                    result["security_checks"] = {}



                    # TLS Version Check

                    if result["tls_version"] in [
                        "TLSv1",
                        "TLSv1.1"
                    ]:

                        result["security_checks"]["tls_version"] = {
                            "status": "weak",
                            "severity": "Medium",
                            "message": "Old TLS version detected"
                        }

                    else:

                        result["security_checks"]["tls_version"] = {
                            "status": "secure",
                            "severity": "None",
                            "message": "Modern TLS version"
                        }



                    # Cipher Check

                    cipher_name = result["cipher"][0]


                    weak_ciphers = [

                        "RC4",
                        "DES",
                        "3DES",
                        "NULL",
                        "EXPORT"

                    ]


                    cipher_status = "secure"


                    for cipher in weak_ciphers:

                        if cipher in cipher_name:

                            cipher_status = "weak"



                    if cipher_status == "weak":

                        result["security_checks"]["cipher"] = {

                            "status": "weak",

                            "severity": "Medium",

                            "message": "Weak cipher detected"

                        }

                    else:

                        result["security_checks"]["cipher"] = {

                            "status": "secure",

                            "severity": "None",

                            "message": "Secure cipher"

                        }



                    # Certificate Expiry Check

                    if result["days_remaining"] < 30:

                        result["security_checks"]["certificate_expiry"] = {

                            "status": "warning",

                            "severity": "Medium",

                            "message": "Certificate expires soon"

                        }

                    else:

                        result["security_checks"]["certificate_expiry"] = {

                            "status": "secure",

                            "severity": "None",

                            "message": "Certificate validity is good"

                        }



            return {
                "scanner": "SSLLookup",
                "target": self.host,
                "status": "success",
                "data": result
            }



        except ssl.SSLCertVerificationError as e:


            return {
                "scanner": "SSLLookup",
                "target": self.host,
                "status": "success",
                "data": {
                    "certificate_status": "certificate failed verification",
                    "message": str(e)
                }
            }



        except socket.timeout:


            return {
                "scanner": "SSLLookup",
                "target": self.host,
                "status": "success",
                "data": {
                    "certificate_status": "connection timeout",
                    "message": "Unable to connect to SSL service"
                }
            }



        except Exception as e:


            return {
                "scanner": "SSLLookup",
                "target": self.host,
                "status": "failed",
                "error": str(e)
            }
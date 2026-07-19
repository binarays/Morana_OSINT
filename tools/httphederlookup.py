import requests


class HeaderLookup:


    security_headers = [

        "Strict-Transport-HSTS",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy",
        "Permissions-Policy"

    ]


    def __init__(self, domain):

        self.domain = domain


    def scan(self):

        result = {}


        try:

            url = self.domain

            if not url.startswith("http"):

                url = "https://" + url


            response = requests.get(
                url,
                timeout=10,
                allow_redirects=True
            )


            headers = dict(response.headers)


            result["server"] = headers.get(
                "Server",
                "Unknown"
            )


            result["status_code"] = response.status_code



            # Check HTTPS redirect

            result["https_status"] = {}

            if response.url.startswith("https://"):

                result["https_status"] = {

                    "status": "secure",

                    "message": "HTTPS enabled"

                }

            else:

                result["https_status"] = {

                    "status": "warning",

                    "severity": "Medium",

                    "message": "HTTPS not enforced"

                }



            result["security_headers"] = {}


            result["security_findings"] = []



            for header in self.security_headers:


                if header in headers:


                    result["security_headers"][header] = "Present"



                else:


                    result["security_headers"][header] = "Missing"



                    severity = "Low"


                    if header == "Content-Security-Policy":

                        severity = "Medium"


                    elif header == "Strict-Transport-Security":

                        severity = "Medium"



                    result["security_findings"].append({

                        "header": header,

                        "status": "Missing",

                        "severity": severity,

                        "message": f"{header} header is missing"

                    })



            # Server information disclosure

            if result["server"] != "Unknown":


                result["security_findings"].append({

                    "finding": "Server Version Disclosure",

                    "severity": "Low",

                    "message": "Server header exposes information"

                })



            return {

                "scanner": "HeaderLookup",

                "target": self.domain,

                "status": "success",

                "data": result

            }



        except Exception as e:


            return {

                "scanner": "HeaderLookup",

                "target": self.domain,

                "status": "failed",

                "error": str(e)

            }
import requests


class HeaderLookup:


    security_headers = [

        "Strict-Transport-Security",
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
                timeout=10
            )


            headers = dict(response.headers)


            result["server"] = headers.get(
                "Server",
                "Unknown"
            )


            result["status_code"] = response.status_code


            result["security_headers"] = {}


            for header in self.security_headers:

                if header in headers:

                    result["security_headers"][header] = "Present"

                else:

                    result["security_headers"][header] = "Missing"



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
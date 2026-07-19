import requests


class RobotsLookup:


    def __init__(self, domain):

        self.domain = domain



    def scan(self):

        result = {

            "found": False,

            "paths": []

        }


        try:

            url = self.domain


            if not url.startswith("http"):

                url = "https://" + url


            robots_url = url + "/robots.txt"


            response = requests.get(
                robots_url,
                timeout=10
            )


            if response.status_code == 200:


                result["found"] = True


                for line in response.text.splitlines():

                    if line.lower().startswith(
                        "disallow:"
                    ):

                        path = line.split(
                            ":",
                            1
                        )[1].strip()


                        if path:

                            result["paths"].append(
                                path
                            )


            return {

                "scanner":"RobotsLookup",

                "target":self.domain,

                "status":"success",

                "data":result

            }



        except Exception as e:


            return {

                "scanner":"RobotsLookup",

                "target":self.domain,

                "status":"failed",

                "error":str(e)

            }
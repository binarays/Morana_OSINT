import requests
from bs4 import BeautifulSoup


class TechLookup:


    def __init__(self, domain):

        self.domain = domain



    def scan(self):

        result = {

            "server": None,

            "frameworks": [],

            "cms": []

        }


        try:

            url = self.domain


            if not url.startswith("http"):

                url = "https://" + url



            response = requests.get(
                url,
                timeout=10
            )


            headers = response.headers


            result["server"] = headers.get(
                "Server",
                "Unknown"
            )


            html = response.text.lower()


            # CMS detection

            if "wp-content" in html:

                result["cms"].append(
                    "WordPress"
                )


            # Framework detection

            if "react" in html:

                result["frameworks"].append(
                    "React"
                )


            if "vue" in html:

                result["frameworks"].append(
                    "Vue"
                )


            soup = BeautifulSoup(
                html,
                "html.parser"
            )


            scripts = soup.find_all(
                "script"
            )


            for script in scripts:

                src = script.get("src")

                if src:

                    if "jquery" in src:

                        result["frameworks"].append(
                            "jQuery"
                        )


            return {

                "scanner": "TechnologyLookup",

                "target": self.domain,

                "status": "success",

                "data": result

            }



        except Exception as e:


            return {

                "scanner":"TechnologyLookup",

                "target":self.domain,

                "status":"failed",

                "error":str(e)

            }
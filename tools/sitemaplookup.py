import requests
import xml.etree.ElementTree as ET


class SitemapLookup:


    def __init__(self, domain):

        self.domain = domain



    def scan(self):

        result = {

            "found":False,

            "urls":[]

        }


        try:

            url = self.domain


            if not url.startswith("http"):

                url = "https://" + url



            sitemap = url + "/sitemap.xml"



            response = requests.get(
                sitemap,
                timeout=10
            )



            if response.status_code == 200:


                result["found"] = True


                root = ET.fromstring(
                    response.text
                )


                for item in root.iter():

                    if item.tag.endswith(
                        "loc"
                    ):

                        result["urls"].append(
                            item.text
                        )


            return {

                "scanner":"SitemapLookup",

                "target":self.domain,

                "status":"success",

                "data":result

            }



        except Exception as e:


            return {

                "scanner":"SitemapLookup",

                "target":self.domain,

                "status":"failed",

                "error":str(e)

            }
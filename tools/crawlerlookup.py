import requests

from bs4 import BeautifulSoup

from urllib.parse import urljoin, urlparse



class Crawler:


    def __init__(self, domain):

        self.domain = domain

        self.visited = set()

        self.forms = []

        self.pages = {}



    def crawl_page(self, url, callback=None):


        if url in self.visited:

            return []


        self.visited.add(url)


        if callback:

            callback(
                f"Crawling: {url}"
            )


        links = []


        try:


            response = requests.get(
                url,
                timeout=10
            )


            self.pages[url] = {

                "status_code":
                response.status_code

            }


            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )



            # Find forms for future vulnerability scanning

            for form in soup.find_all(
                "form"
            ):

                self.forms.append({

                    "url": url,

                    "method":
                    form.get(
                        "method",
                        "GET"
                    ),

                    "action":
                    form.get(
                        "action"
                    )

                })



            for link in soup.find_all(
                "a",
                href=True
            ):


                full_url = urljoin(
                    url,
                    link["href"]
                )


                parsed_url = urlparse(
                    full_url
                )


                current_domain = urlparse(
                    url
                ).netloc



                # Same domain only

                if parsed_url.netloc == current_domain:


                    # Ignore files

                    if not full_url.lower().endswith(
                        (
                            ".jpg",
                            ".png",
                            ".pdf",
                            ".zip",
                            ".css",
                            ".js"
                        )
                    ):

                        links.append(
                            full_url
                        )


        except Exception:

            pass


        return links



    def scan(self, callback=None):


        try:


            url = self.domain


            if not url.startswith(
                "http"
            ):

                url = "https://" + url



            queue = [url]



            while queue and len(self.visited) < 100:


                current = queue.pop(0)


                new_links = self.crawl_page(
                    current,
                    callback
                )


                for link in new_links:


                    if (

                        link not in self.visited

                        and link not in queue

                    ):

                        queue.append(
                            link
                        )



            return {

                "scanner":"Crawler",

                "target":self.domain,

                "status":"success",

                "data":{

                    "pages_found":
                    list(self.visited),


                    "page_details":
                    self.pages,


                    "forms":
                    self.forms

                }

            }



        except Exception as e:


            return {

                "scanner":"Crawler",

                "target":self.domain,

                "status":"failed",

                "error":str(e)

            }
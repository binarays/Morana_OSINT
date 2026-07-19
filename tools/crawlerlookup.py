import requests

from bs4 import BeautifulSoup

from urllib.parse import urljoin, urlparse



class Crawler:


    def __init__(self, domain):

        self.domain = domain

        self.visited = set()



    def crawl_page(self, url):


        if url in self.visited:

            return []


        self.visited.add(url)


        links = []


        try:


            response = requests.get(
                url,
                timeout=10
            )


            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )


            for link in soup.find_all(
                "a",
                href=True
            ):


                full_url = urljoin(
                    url,
                    link["href"]
                )


                if urlparse(full_url).netloc == urlparse(url).netloc:

                    links.append(
                        full_url
                    )


        except Exception:

            pass


        return links



    def scan(self):


        try:


            url = self.domain


            if not url.startswith("http"):

                url = "https://" + url



            queue = [url]


            while queue and len(self.visited) < 100:


                current = queue.pop(0)


                new_links = self.crawl_page(
                    current
                )


                queue.extend(
                    new_links
                )



            return {

                "scanner":"Crawler",

                "target":self.domain,

                "status":"success",

                "data":{

                    "pages_found":
                    list(self.visited)

                }

            }



        except Exception as e:


            return {

                "scanner":"Crawler",

                "target":self.domain,

                "status":"failed",

                "error":str(e)

            }
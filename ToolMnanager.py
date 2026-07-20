from tools.dnslookup import DNSLookup
from tools.ssllookup import SSLLookup
from tools.portlookup.fullportlookup import FullPortLookup
from tools.portlookup.quickportlookup import QuickPortLookup
from tools.whoislookup import WhoisLookup
from tools.httphederlookup import HeaderLookup
from tools.techlookup import TechLookup
from tools.botlookup import RobotsLookup
from tools.sitemaplookup import SitemapLookup
from tools.crawlerlookup import Crawler


class ToolManager:


    def __init__(self, domain, PortLookupType="quick"):

        self.tools = [

            DNSLookup(domain),
            SSLLookup(domain),
            WhoisLookup(domain),
            HeaderLookup(domain),
            TechLookup(domain),
            RobotsLookup(domain),
            SitemapLookup(domain),
            Crawler(domain)
        ]

        if PortLookupType == "full":

            self.tools.insert(
                2,
                FullPortLookup(domain)
            )


        else:

            self.tools.insert(
                2,
                QuickPortLookup(domain)
            )


    def scan(self):

        result = {}


        for tool in self.tools:

            result[tool.__class__.__name__] = tool.scan()


        return result
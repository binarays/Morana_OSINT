from tools.dnslookup import dnstool
from tools.ssllookup import ssltool

class ToolManager:

    def __init__(self, domain):
        self.tools=[
            dnstool(domain),
            ssltool(domain)
        ]
    
    def scan(self):
        result=[]

        for tool in self.tools:
            result[tool.__class__.__name__]=tool.scan()

        return result
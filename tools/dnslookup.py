import dns.resolver

class dnstool:
    records=["A","AAAA","MX","NS","TXT","CNAME","SOA"]

    def __init__(self,domain):
        self.domain=domain
    
    def dnsscan(self):
        result={}

        for record in self.records:
            try:
                output=dns.resolver.resolve(self.domain,record)
                result[record]=[str(answer) for answer in output]
            
            except dns.resolver.NoAnswer:
                result[record]=[]
            
            except dns.renderer.NXDOMAIN:
                result=["error"]="Domain does not exist."
            
            except Exception as e:
                result[record]=f"Error: {e}"

        return result
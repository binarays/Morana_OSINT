import dns.resolver


class DNSLookup:

    records = [
        "A",
        "AAAA",
        "MX",
        "NS",
        "TXT",
        "CNAME",
        "SOA"
    ]


    def __init__(self, domain):
        self.domain = domain


    def scan(self):

        result = {}


        try:

            for record in self.records:

                try:

                    output = dns.resolver.resolve(
                        self.domain,
                        record
                    )

                    result[record] = [
                        str(answer)
                        for answer in output
                    ]


                except dns.resolver.NoAnswer:

                    result[record] = []


                except dns.resolver.NXDOMAIN:

                    return {
                        "scanner": "DNSLookup",
                        "target": self.domain,
                        "status": "failed",
                        "error": "Domain does not exist."
                    }


                except Exception as e:

                    result[record] = f"Error: {e}"


            return {
                "scanner": "DNSLookup",
                "target": self.domain,
                "status": "success",
                "data": result
            }


        except Exception as e:

            return {
                "scanner": "DNSLookup",
                "target": self.domain,
                "status": "failed",
                "error": str(e)
            }
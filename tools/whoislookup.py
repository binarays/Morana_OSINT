import whois
import requests


class WhoisLookup:

    def __init__(self, domain):
        self.domain = domain


    def clean_value(self, value):

        if isinstance(value, list):
            return [
                str(item)
                for item in value
            ]

        if value:
            return str(value)

        return None



    def rdap_lookup(self):

        try:

            url = f"https://rdap.org/domain/{self.domain}"


            response = requests.get(
                url,
                timeout=10
            )


            if response.status_code != 200:

                return None



            data = response.json()


            result = {}


            result["handle"] = data.get(
                "handle"
            )


            result["status"] = self.clean_value(
                data.get("status")
            )


            result["name_servers"] = [
                ns.get("ldhName")
                for ns in data.get(
                    "nameservers",
                    []
                )
            ]



            for entity in data.get(
                "entities",
                []
            ):

                if "registrar" in entity.get(
                    "roles",
                    []
                ):

                    result["registrar"] = (
                        entity.get("handle")
                    )



            return result



        except Exception:

            return None



    def scan(self):

        result = {}


        try:

            output = whois.whois(
                self.domain
            )


            if output:


                result["registrar"] = self.clean_value(
                    output.registrar
                )


                result["creation_date"] = self.clean_value(
                    output.creation_date
                )


                result["expiration_date"] = self.clean_value(
                    output.expiration_date
                )


                result["updated_date"] = self.clean_value(
                    output.updated_date
                )


                result["name_servers"] = self.clean_value(
                    output.name_servers
                )


                result["status"] = self.clean_value(
                    output.status
                )


                result["country"] = self.clean_value(
                    output.country
                )


                return {
                    "scanner": "WhoisLookup",
                    "target": self.domain,
                    "status": "success",
                    "source": "WHOIS",
                    "data": result
                }



            # WHOIS failed → RDAP fallback

            rdap = self.rdap_lookup()



            if rdap:


                return {
                    "scanner": "WhoisLookup",
                    "target": self.domain,
                    "status": "success",
                    "source": "RDAP",
                    "data": rdap
                }



            return {
                "scanner": "WhoisLookup",
                "target": self.domain,
                "status": "unavailable",
                "message": "Registration data is not available in public sources",
                "data": {}
            }



        except Exception as e:


            rdap = self.rdap_lookup()


            if rdap:

                return {
                    "scanner": "WhoisLookup",
                    "target": self.domain,
                    "status": "success",
                    "source": "RDAP",
                    "data": rdap
                }



            return {
                "scanner": "WhoisLookup",
                "target": self.domain,
                "status": "unavailable",
                "message": "Registration data is not available in public sources",
                "data": {}
            }
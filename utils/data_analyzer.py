class FindingAnalyzer:


    def analyze(self, results):

        findings = []


        self.check_headers(
            results,
            findings
        )


        self.check_ssl(
            results,
            findings
        )


        self.check_ports(
            results,
            findings
        )


        self.check_crawler(
            results,
            findings
        )


        self.check_technology(
            results,
            findings
        )


        self.check_dns(
            results,
            findings
        )


        return findings



    def check_headers(self, results, findings):


        header = results.get(
            "HeaderLookup"
        )


        if not header:
            return


        if header.get("status") != "success":
            return


        headers = header.get(
            "data",
            {}
        ).get(
            "security_headers",
            {}
        )


        for name, status in headers.items():


            if status == "Missing":


                severity = "Low"


                if name == "Content-Security-Policy":

                    severity = "Medium"



                elif name == "Strict-Transport-Security":

                    severity = "Medium"



                elif name == "X-Frame-Options":

                    severity = "Low"



                findings.append({

                    "title":
                    f"Missing {name} header",


                    "severity":
                    severity,


                    "category":
                    "Security Configuration",


                    "description":
                    f"{name} security header is missing"


                })





    def check_ssl(self, results, findings):


        ssl = results.get(
            "SSLLookup"
        )


        if not ssl:
            return


        if ssl.get("status") != "success":
            return



        data = ssl.get(
            "data",
            {}
        )


        days = data.get(
            "Days Remaining"
        )



        if days is not None:


            if days < 0:


                findings.append({

                    "title":
                    "Expired SSL Certificate",


                    "severity":
                    "High",


                    "category":
                    "SSL/TLS",


                    "description":
                    "SSL certificate has expired"

                })



            elif days < 30:


                findings.append({

                    "title":
                    "SSL Certificate Expiring Soon",


                    "severity":
                    "Medium",


                    "category":
                    "SSL/TLS",


                    "description":
                    "Certificate expires within 30 days"

                })



        tls = data.get(
            "TLS Version"
        )


        if tls in [

            "TLSv1",
            "TLSv1.1"

        ]:


            findings.append({

                "title":
                "Weak TLS Version",


                "severity":
                "Medium",


                "category":
                "SSL/TLS",


                "description":
                f"Old TLS version detected: {tls}"

            })





    def check_ports(self, results, findings):


        ports = results.get(
            "PortLookup"
        )


        if not ports:
            return



        if ports.get("status") != "success":
            return



        data = ports.get(
            "data",
            []
        )


        dangerous_ports = {


            21:"FTP service exposed",

            23:"Telnet service exposed",

            3306:"MySQL database exposed",

            3389:"RDP service exposed",

            5432:"PostgreSQL database exposed"


        }



        for port in data:


            port_number = port.get(
                "port"
            )


            if port_number in dangerous_ports:


                findings.append({

                    "title":
                    dangerous_ports[port_number],


                    "severity":
                    "High",


                    "category":
                    "Network Exposure",


                    "description":
                    f"Port {port_number} is publicly accessible"

                })





    def check_crawler(self, results, findings):


        crawler = results.get(
            "Crawler"
        )


        if not crawler:
            return


        if crawler.get("status") != "success":
            return



        pages = crawler.get(
            "data",
            {}
        ).get(
            "pages_found",
            []
        )



        sensitive_paths = [

            "admin",
            "backup",
            "config",
            "phpmyadmin",
            ".git"

        ]



        for page in pages:


            for path in sensitive_paths:


                if path in page.lower():


                    findings.append({

                        "title":
                        "Potential Sensitive Path Exposed",


                        "severity":
                        "High",


                        "category":
                        "Information Exposure",


                        "description":
                        f"Sensitive path found: {page}"

                    })





    def check_technology(self, results, findings):


        tech = results.get(
            "TechnologyLookup"
        )


        if not tech:
            return



        if tech.get("status") != "success":
            return



        data = tech.get(
            "data",
            {}
        )


        if data.get("server") not in [

            None,
            "Unknown"

        ]:


            findings.append({

                "title":
                "Server Information Disclosure",


                "severity":
                "Low",


                "category":
                "Information Disclosure",


                "description":
                f"Server detected: {data.get('server')}"

            })





    def check_dns(self, results, findings):


        dns = results.get(
            "DNSLookup"
        )


        if not dns:
            return



        if dns.get("status") != "success":
            return



        findings.append({

            "title":
            "DNS Information Collected",


            "severity":
            "Information",


            "category":
            "Reconnaissance",


            "description":
            "DNS records successfully discovered"

        })
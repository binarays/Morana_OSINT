from PyQt6.QtCore import (
    QThread,
    pyqtSignal
)
from ToolMnanager import ToolManager
from utils.story import HistoryManager
from utils.data_analyzer import FindingAnalyzer
import time



class ScanWorker(QThread):


    progress = pyqtSignal(str)

    finished = pyqtSignal(dict)



    def __init__(self,domain, port_lookup_type="quick"):

        super().__init__()

        self.domain = domain
        self.port_lookup_type = port_lookup_type



    def run(self):

        try:


            self.progress.emit(
                "Starting scanner..."
            )


            manager = ToolManager(
                self.domain, self.port_lookup_type
            )


            result = {}


            FRIENDLY_MESSAGES = {
                "DNSLookup":        "Looking for DNS information...",
                "SSLLookup":        "Checking SSL certificate and security...",
                "QuickPortLookup":  "Scanning common ports (quick)...",
                "FullPortLookup":   "Scanning all ports (this may take a while)...",
                "HeaderLookup":     "Fetching HTTP headers and security policies...",
                "WhoisLookup":      "Retrieving WHOIS registration details...",
                "TechLookup":       "Detecting technologies and frameworks...",
                "RobotsLookup":     "Reading robots.txt and sitemap hints...",
                "SitemapLookup":    "Exploring sitemap structure...",
                "Crawler":          "Crawling pages and mapping site structure...",
            }

            for tool in manager.tools:

                tool_name = tool.__class__.__name__
                msg = FRIENDLY_MESSAGES.get(tool_name, f"Running {tool_name}...")
                self.progress.emit(msg)


                scan_result = tool.scan()
                
                time.sleep(2)


                result[
                    tool.__class__.__name__
                ] = scan_result

                self.progress.emit(
                    f"{tool.__class__.__name__} completed"
                )



            analyzer = FindingAnalyzer()
            findings = analyzer.analyze(result)
            result["Findings"] = findings

            # Save history

            history = HistoryManager()

            history.save_scan(
                result, self.domain
            )


            self.finished.emit(
                result
            )



        except Exception as e:


            self.finished.emit(
                {
                    "error":str(e)
                }
            )
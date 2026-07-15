from PyQt6.QtCore import (
    QThread,
    pyqtSignal
)
from ToolMnanager import ToolManager
from utils.story import HistoryManager
import time



class ScanWorker(QThread):


    progress = pyqtSignal(str)

    finished = pyqtSignal(dict)



    def __init__(self,domain):

        super().__init__()

        self.domain = domain



    def run(self):

        try:


            self.progress.emit(
                "Starting scanner..."
            )


            manager = ToolManager(
                self.domain
            )


            result = {}


            for tool in manager.tools:


                self.progress.emit(
                    f"Running {tool.__class__.__name__}..."
                )


                scan_result = tool.scan()
                
                time.sleep(2)


                result[
                    tool.__class__.__name__
                ] = scan_result




                self.progress.emit(
                    f"{tool.__class__.__name__} completed"
                )



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
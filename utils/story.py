import json
import os
from datetime import datetime


SOTORY_FILE = "recent/scan_story.json"


class HistoryManager:


    def save_scan(self, result, domain="Unknown"):

        story = []


        # Check existing history
        if os.path.exists(SOTORY_FILE):

            try:

                with open(
                    SOTORY_FILE,
                    "r"
                ) as file:

                    story = json.load(file)

            except json.JSONDecodeError:

                story = []



        scanrec = {

            "scan_id": len(story) + 1,

            "time": datetime.now().isoformat(),

            "domain": domain,

            "result": result

        }


        story.append(scanrec)



        # Create folder if not exists
        folder = os.path.dirname(SOTORY_FILE)

        if folder:
            os.makedirs(
                folder,
                exist_ok=True
            )


        with open(
            SOTORY_FILE,
            "w"
        ) as file:

            json.dump(
                story,
                file,
                indent=4
            )


        return scanrec



    def get_history(self):

        if not os.path.exists(SOTORY_FILE):

            return []


        with open(
            SOTORY_FILE,
            "r"
        ) as f:

            return json.load(f)

    def delete_scan(self, scan_id):
        history = self.get_history()
        new_history = [item for item in history if item.get("scan_id") != scan_id]
        with open(SOTORY_FILE, "w") as file:
            json.dump(new_history, file, indent=4)
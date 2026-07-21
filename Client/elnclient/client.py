import requests, os, mimetypes

class ElnClient:
    """Used for pushing info directly to the ELN
    """
    def __init__(self, url: str, api_key: str, title: str, desc: str):
        self.url = url
        self.api_key = api_key

        # Useful variables:
        self.title = title
        self.desc = desc
        self.id = None

        self.headers = {
            "Authorization": f"{self.api_key}",
            "Content-Type": "application/json"
        }

        data = {    #This defines who can read/write to the experiment in the ELN (30=anyone)
            "canwrite": "{\"base\":30,\"teams\":[],\"teamgroups\":[],\"users\":[]}",
            "title": title,
            "body": desc
        }

        r = requests.post(f"{self.url}/experiments/", headers=self.headers, json=data)
        if r.status_code != 201:
            raise RuntimeWarning(f"Error code: {r.status_code}\nCould not send this following data:\n{data}")
        
        self.id = int(r.headers["Location"].split('/')[-1]) # get the id from the last bit of the url
        print(f"[ELN] Successfully added experiment:\nTitle: {self.title}\nDescription: {self.desc}\nID: {self.id}\n")
        return
    
    def upload_file(self, file_path: str, comment: str | None):
        """Uploads a png or jpg image to the eln experiment

        Args:
            file_path (str): Filepath of the image you would like to upload
            comment (str | None): Image comment

        Raises:
            ValueError: File path led to a file that does not exists or is invalid
            ValueError: _description_

        Returns:
            request: Returns POST request response 
        """
        if not os.path.isfile(file_path):
            print(f"[ELN] ERROR - File not found at {file_path}, skipping")
            return

        # Requires a different header because of how images are handled
        upload_headers = {"Authorization": self.api_key}

        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            files = {'file': (filename, f)}
            data = {"comment": comment} if comment else {}

            r = requests.post(
                f"{self.url}/experiments/{self.id}/uploads",
                headers=upload_headers,
                files=files,
                data=data
            )
        
        if r.status_code != 201: print(f'[ELN] Error adding {filename}')
        else: print(f'[ELN] Successfully added {filename} to experiment {self.id}')
        return r
    
    def add_step(self, step: str):
        """Adds a step to the current experiment

        Args:
            step (str): Step description
        """
        r = requests.post(f"{self.url}/experiments/{self.id}/steps", headers=self.headers, json={"body": step})
        if r.status_code == 201:
            print(f"[ELN] Added step: {step}")
        return
import requests
import json

class GithubManager:
    """
    Class for managing Github for the projects
    """
    def __init__(self, access_token, repo_name, repo_description) -> None:
        self.access_token = access_token
        self.repo_name = repo_name
        self.repo_description = repo_description

        self.api_url = 'https://api.github.com/user/repos'
        self.headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def create_github_repo(self):
        data = {
            'name': self.repo_name,
            'description': self.repo_description,
            'auto_init': False  # This creates an initial commit with empty README
        }
        response = requests.post(self.api_url, headers=self.headers, data=json.dumps(data))

        if response.status_code == 201:
            print('Successfully created repository')
        else:
            print('Failed to create repository')

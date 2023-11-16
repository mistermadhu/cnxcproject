
from github import Github

# Authentication is defined via github.Auth
from github import Auth

import json

class GitUtility:
    def __init__(self):
        # using an access token
        self.auth = Auth.Token("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")

        # Public Web Github
        self.git_client = Github(auth=self.auth)

    def getAllRepos(self):
    # Github Enterprise with custom hostname
    #self.git_client = Github(auth=self.auth, base_url="https://github.com/mistermadhu/api/v3"

        repo_list=[]
        for repo in self.git_client.get_user().get_repos():
            print(repo.name)
            repo_list.append(repo.name)
        
        return json.dumps(repo_list)
    
    def pushTheFileToRepo(self,test_script):
    # Create a new file in repo
        try:
            repo = self.git_client.get_repo(test_script.repo_url) #mistermadhu/cnxcproject
            repo.create_file(test_script.name,test_script.commit_message, test_script.content, branch=test_script.branch)           
            self.git_client.close()
            return "Test scrip pushed successfully"
        except Exception as e:
            return e
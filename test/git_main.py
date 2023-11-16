
from github import Github

# Authentication is defined via github.Auth
from github import Auth

# using an access token
auth = Auth.Token("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")

# Public Web Github
g = Github(auth=auth)

# Github Enterprise with custom hostname
#g = Github(auth=auth, base_url="https://github.com/mistermadhu/api/v3")


for repo in g.get_user().get_repos():
    print(repo.name)
 
 
 # Create a new file in repo
repo = g.get_repo("mistermadhu/cnxcproject")
repo.create_file("genai_sample_script.txt", "test", "best", branch="main")
    
g.close()
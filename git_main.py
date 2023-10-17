
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
 
    
g.close()
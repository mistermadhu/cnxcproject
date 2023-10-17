import requests,json,io
from bs4 import BeautifulSoup

base_url="https://cnxcta.atlassian.net/rest/api/3/search"
user="mistermadhu@gmail.com"
pwd="ATATT3xFfGF0eC4whGYnZUoaxyJd5ZQJeJ-PgjsSZDxLG_um5ZLC-oV1g2ImKDZEg15Rid0Fb1weIdfJyNpXM1kPyULaKflaHJ1VQTCDp5IZCs_W-ZSVbN4EM4LgjOB_zFQwM2FXdOO-4MsZ1hk5CYkKmfv0HOi555yupGlCWfadxWS2kJf0iPc=24D25812"
project_key="CNXCClient"


headers={
    "Accept":"application/json",
    "Content-Type":"application/json"
}

api_url=f"{base_url}?jql=project={project_key}"
#to get the total number of issues

response=requests.get(api_url,headers=headers,auth=(user,pwd))
data=response.json()
total=data["total"]

#setup the pagination
batch_size=100
nor=(total+batch_size-1)//batch_size
print(nor)

#looping
all=[]
for n in range(nor):
    s=n*batch_size
    query={
        "jql":"project=CNXCClient",
        "startAt":s,
        "maxResults":batch_size
    }
    response=requests.get(base_url,headers=headers,params=query,auth=(user,pwd))
    data=response.json()
    print(data)
    issues=data.get("issues",[])
    all.extend(issues)
with io.open("results.csv","w",encoding="utf-8")as f1:
    for one in all:
        f1.write(one["id"]+","+one["key"]+","+str(one["fields"]["description"])+"\n")
        #f1.write(one["id"]+","+one["key"]+","+BeautifulSoup(str(one["fields"]["description"]), 'html.parser').get_text()+"\n")
    f1.close()
    
    
    
    import requests


# Fetch description of the issue

# Your JIRA instance URL and API token
jira_url = "https://cnxcta.atlassian.net"
api_token = pwd

# JIRA user story key (e.g., "PROJECT-123")
issue_key = "CNXCCLIEN-2"

# URL for the JIRA REST API to fetch the issue details
api_url = f"{jira_url}/rest/api/3/issue/{issue_key}"


# Send a GET request to fetch the issue details
response = requests.get(api_url, headers=headers,auth=(user,pwd))

# Check the response
if response.status_code == 200:
    issue_details = response.json()
    rich_text_content = issue_details["fields"]["description"]["content"][0]["content"]
    rich_text_html = " ".join([item["text"] for item in rich_text_content])
    plain_text = BeautifulSoup(rich_text_html, "html.parser").get_text()
    print("User Story Description:")
    print(plain_text)
else:
    print(f"Failed to fetch issue description. Status code: {response.status_code}")
    
    

# Update Acceptance criteria into JIRA 


issue_key = "CNXCCLIEN-5"
api_url = f"{jira_url}/rest/api/2/issue/{issue_key}"    # Using REST API - 2
# New acceptance criteria
new_acceptance_criteria = "Updated acceptance criteria for this user story."

# Create a JSON payload with the new acceptance criteria
payload = {
    "fields": {
        "customfield_10037": new_acceptance_criteria
        # Replace "customfield_12345" with the actual custom field ID for acceptance criteria in your JIRA instance
    }
   
}

print(api_url)
# Send a PUT request to update the issue with the new acceptance criteria
response = requests.put(api_url, data=json.dumps(payload), headers=headers,auth=(user,pwd))
print(response)

# Check the response
if response.status_code == 204:
    print("Acceptance criteria updated successfully.")
else:
    print(f"Failed to update acceptance criteria. Status code: {response.status_code}")


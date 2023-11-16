import requests,json,io
from bs4 import BeautifulSoup
class JIRAUtility:
    def __init__(self):
        self.jira_url = "https://cnxcta.atlassian.net"
        self.base_url=f"{self.jira_url}/rest/api/3/search"
        self.user="mistermadhu@gmail.com"
        #self.self.pwd="ATATT3xFfGF0eC4whGYnZUoaxyJd5ZQJeJ-PgjsSZDxLG_um5ZLC-oV1g2ImKDZEg15Rid0Fb1weIdfJyNpXM1kPyULaKflaHJ1VQTCDp5IZCs_W-ZSVbN4EM4LgjOB_zFQwM2FXdOO-4MsZ1hk5CYkKmfv0HOi555yupGlCWfadxWS2kJf0iPc=24D25812"
        self.pwd="ATATT3xFfGF0LvtY7nr1xP05YeWNtLRDU33wNmp6oVTS-GXD5bNtiJd27r16I5RIy8pt3IbER_hWCWXdhyKAoDanX_3iyJwb80xFqyIozMjrMi55ygrCDjdYwyZ-D4FJ7p_jHodsMPB_gA8VkJFbgfPXEgmK3FVBBK7oD-Np-2moc4QucscqOpg=C1510ED6"
        self.project_key="CNXCClient"

        #JiraAPIToken1
        #ATATT3xFfGF0LvtY7nr1xP05YeWNtLRDU33wNmp6oVTS-GXD5bNtiJd27r16I5RIy8pt3IbER_hWCWXdhyKAoDanX_3iyJwb80xFqyIozMjrMi55ygrCDjdYwyZ-D4FJ7p_jHodsMPB_gA8VkJFbgfPXEgmK3FVBBK7oD-Np-2moc4QucscqOpg=C1510ED6

        self.headers={
            "Accept":"application/json",
            "Content-Type":"application/json"
        }

        self.api_url=f"{self.base_url}?jql=project={self.project_key}"
        #to get the total number of issues

    def fetchAllTicketsFromJIRA(self):
        response=requests.get(self.api_url,headers=self.headers,auth=(self.user,self.pwd))
        data=response.json()
        print (data)
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
            response=requests.get(self.base_url,headers=self.headers,params=query,auth=(self.user,self.pwd))
            data=response.json()
            print(data)
            issues=data.get("issues",[])
            all.extend(issues)
        with io.open("results.csv","w",encoding="utf-8")as f1:
            for one in all:
                f1.write(one["id"]+","+one["key"]+","+str(one["fields"]["description"])+"\n")
                #f1.write(one["id"]+","+one["key"]+","+BeautifulSoup(str(one["fields"]["description"]), 'html.parser').get_text()+"\n")
            f1.close()
        
        return
        



    # Fetch description of the issue
    def fetchIssueDescription(self):
        # Your JIRA instance URL and API token
        api_token = self.pwd

        # JIRA user story key (e.g., "PROJECT-123")
        issue_key = "CNXCCLIEN-2"

        # URL for the JIRA REST API to fetch the issue details
        self.api_url = f"{self.jira_url}/rest/api/3/issue/{issue_key}"


        # Send a GET request to fetch the issue details
        response = requests.get(self.api_url, headers=self.headers,auth=(self.user,self.pwd))

        # Check the response
        if response.status_code == 200:
            issue_details = response.json()
            rich_text_content = issue_details["fields"]["description"]["content"][0]["content"]
            rich_text_html = " ".join([item["text"] for item in rich_text_content])
            plain_text = BeautifulSoup(rich_text_html, "html.parser").get_text()
            print("User Story Description:")
            print(plain_text)
            return plain_text
        else:
            print(f"Failed to fetch issue description. Status code: {response.status_code}")
            return response.status_code
            
        
        

    # Update Acceptance criteria into JIRA 
    def updateAcceptanceCriteria(self):

        issue_key = "CNXCCLIEN-5"
        self.api_url = f"{self.jira_url}/rest/api/2/issue/{issue_key}"    # Using REST API - 2
        # New acceptance criteria
        new_acceptance_criteria = "Updated acceptance criteria for this user story in our JIRA"

        # Create a JSON payload with the new acceptance criteria
        payload = {
            "fields": {
                "customfield_10037": new_acceptance_criteria
                # Replace "customfield_12345" with the actual custom field ID for acceptance criteria in your JIRA instance
            }
        
        }

        print(self.api_url)
        # Send a PUT request to update the issue with the new acceptance criteria
        response = requests.put(self.api_url, data=json.dumps(payload), headers=self.headers,auth=(self.user,self.pwd))
        print(response)

        # Check the response
        if response.status_code == 204:
            print("Acceptance criteria updated successfully.")
            return response
        else:
            print(f"Failed to update acceptance criteria. Status code: {response.status_code}")
            return response.status_code

# Main program
if __name__ == "__main__":
    # Create an instance of the JIRA Utility
    jira_client = JIRAUtility()

    # Call a method
    jira_client.updateAcceptanceCriteria()
 
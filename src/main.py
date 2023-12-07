 
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors  import CORSMiddleware
from decouple import config
from functions.text_to_speech import convert_text_to_speech

# Custom Function imports
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.database import store_messages, reset_messages
from util.jira_utility import JIRAUtility
from util.git_utility import GitUtility
from model.GitModel import TestScript
from util.gen_utility import GeneralUtilty
from util.faker_utility import FakerUtility
# Initiate App
app = FastAPI()

# CORS - Origins
origins =[
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000",
    "http://localhost:3000",
    "*"


]

# CORS - Middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#Check health
@app.get("/health")
async def root():
    print ("Hello madhu")
    return {"message": "Server is healthy"}

# Send prompt
@app.post("/sendprompt/")
async def sendPrompt(prompt_message:str, training_id:str):
 # Get ChatGPT Response
    gp = GeneralUtilty()
    chat_response = get_chat_response(prompt_message, training_id)
    print(chat_response)
    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to chat response")
    return gp.unSeralizeOutput(chat_response)

@app.get("/post-audio-get/")
async def get_audio():
    audio_input=open("voice.mp3", "rb")
 # Decode Audio
    message_decoded=convert_audio_to_text(audio_input)
    print (message_decoded)

 # Guard: Ensure message decoded
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decode audio")
 # Get ChatGPT Response
    chat_response = get_chat_response(message_decoded)
    print(chat_response)
    return chat_response
    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to chat response")

 
@app.post("/post-audio/")
async def post_audio(file:UploadFile=File(...)):
 # Get saved audio
    #audio_input=open("voice.mp3", "rb")

 # Save file form Frontend 
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())

    audio_input= open(file.filename,"rb")
 # Decode Audio
    message_decoded=convert_audio_to_text(audio_input)
    print (message_decoded)

 # Guard: Ensure message decoded
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decode audio")

   # Get ChatGPT Response
    chat_response = get_chat_response(message_decoded)
    print(chat_response)

    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to chat response")

   # Store messages
    store_messages(message_decoded, chat_response)

    #Convert chat response to audio
    audio_output = convert_text_to_speech(chat_response)

    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get Eleven labs audio response")

    # Create a generator that yields chunks of data 
    def iterfile():
        yield audio_output

    # Return audio file
    return StreamingResponse(iterfile(),media_type="application/octet-stream")   

# Reset Conversation
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"response": "conversation reset"}

# Get issues Details
@app.get("/getIssueDetails")
async def get_issueDetails():
  try:
    # Create an instance of the JIRA Utility
    jira_client = JIRAUtility()

    # Call a method to fetch details of the issue.
    return jira_client.fetchIssueDescription()
  except Exception as e:
    return
  

# Get Issue list
@app.get("/getIssueList")
async def get_issueList():
  try:
    # Create an instance of the JIRA Utility
    jira_client = JIRAUtility()

    # Call a method to fetch all tickets from JIRA
    return jira_client.fetchAllTicketsFromJIRA()
  except Exception as e:
    return
  
# Update Acceptance Criteria
@app.put("/updateAcceptanceCriteria")
async def updateAcceptanceCriteria():
  try:
    # Create an instance of the JIRA Utility
    jira_client = JIRAUtility()

    # Call a method to update Acceptance Criteria
    return jira_client.updateAcceptanceCriteria()
  except Exception as e:
    return


# Get All Reports
@app.get("/get-all-repos")
async def getAllRepos():
  try:
    # Create an instance of the Git Utility
    git_client = GitUtility()

    # Call a method to update Acceptance Criteria
    return git_client.getAllRepos()
  except Exception as e:
    return

# Push Test scripts to Git Repo
@app.put("/push-scripts")
async def pushTestScripts(test_script:TestScript):
  try:

    # Create an instance of the Git Utility
    git_client = GitUtility()

    # Call a method to update Acceptance Criteria
    return git_client.pushTheFileToRepo(test_script)
  except Exception as e:
    return

@app.post("/generate-from-openapispec")
async def generateScriptFromOpenapispec(prompt_message:str, training_id:str,file:UploadFile=File(...)):
 # GetScript from Open API Spec
    gp = GeneralUtilty()
 # Save file form Frontend 
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())

    openapispec_file= open(file.filename,"r")
 #  Read Open Api Spec
    print (openapispec_file)

 # Guard: Ensure message decoded
    if not openapispec_file:
        return HTTPException(status_code=400, detail="Failed to open openapi spec")

   # Get ChatGPT Response
    chat_response = get_chat_response(f"{prompt_message}:{openapispec_file.read()}", training_id)
    print(chat_response)

    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to chat response")
    else:
       return gp.unSeralizeOutput(chat_response)

    # Create a generator that yields chunks of data 
    #def iterfile():
    #    yield chat_response

    # Return audio file
   # return  StreamingResponse(iterfile(),media_type="application/octet-stream")   
 

@app.post("/train-model")
async def trainModel(prompt_message:str, title: str):
  gp = GeneralUtilty()
  # Specify the file path and open the file in write mode ("w")
  file_id=gp.getUUID()
  file_path =f"{gp.getTrainingFolder()}/{file_id}.td"
  with open(file_path, "w", encoding="utf-8") as file:
    # Write data to the file
    file.write(prompt_message)

  gp.updateTrainingMappingFile(file_id,title)
  return {"file_id":file_id}

@app.get("/find-trained-model")
async def getTrainedModelId(search_title:str):
  gp = GeneralUtilty()
  return gp.findTitleFuzzyMatch(search_title)

@app.get("/find-all-trained-models")
async def getAllTrainedModels():
  gp = GeneralUtilty()
  return gp.getAllTrainedModels()

@app.get("/fake-data")
async def getFakeData(testdata_type: str):
   fk = FakerUtility()
   return fk.getFakeData(testdata_type)
import openai
from decouple import config
from util.gen_utility import GeneralUtilty


# Retrieve Enviornment Variables
#openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")


# Open AI - Whisper
# Convert audio to text
def convert_audio_to_text(audio_file):
  try:
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    message_text = transcript["text"]
    return message_text
  except Exception as e:
    return

# Open AI - Chat GPT
# Convert audio to text
def get_chat_response(message_input, training_id):
  gu= GeneralUtilty()
  messages=[]
  try:
    messages.append({"role": "system", "content": gu.getTrainingData(training_id)})
  except Exception as e:
    print(f"An unexpected error occurred while finding training data for id {training_id}. Error: {e}")
  pass
  user_message = {"role": "user", "content": message_input }
  messages.append(user_message)
  print(messages)

  try:
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      #model="gpt-4-1106-preview",
      messages=messages
    )
    message_text = response["choices"][0]["message"]["content"]
    return message_text
  except Exception as e:
    print(f"An unexpected error occurred while invoking ChatGPT API. Error: {e}")
    return
  


from fuzzywuzzy import fuzz
import json


# Define the two strings to compare
 
data={
 "44886c84-e451-4040-b5f7-96878f720aaa": "The quick", 
"44886c84-e451-4040-b5f7-96878f720aab": "The quick red fox jumps over the lazy dog.", 
 "44886c84-e451-4040-b5f7-96878f720aac": "I jump over the lazy dog.", 
 "44886c84-e451-4040-b5f7-96878f720aad": "The slow moving fox jumps over the lazy dog", 
 "44886c84-e451-4040-b5f7-96878f720aae": "The quick brown elephant sits on the lazy dog", 
 "40899cbb-a72c-4a81-8591-33799c494b0f": "The quick brown fox jumps over the lazy dog", 
 "8f720e5c-a8b6-4426-b168-e721d073d190": "The slow brown fox flies over the quick cat"
 }

search_title="The quick brown fox"
 

desiredID=""
desiredTitle=""
similarity_score_threshold=50.0
# Loop through the key-value pairs in the dictionary
for key, value in data.items():
    print(f"Key: {key}, Value: {value}")
    similarity_score = fuzz.ratio(search_title, value)
    print(similarity_score)
    if(similarity_score > similarity_score_threshold):
        desiredID=key
        desiredTitle=value
# Calculate the similarity score using the fuzz.ratio function
 
 
print(f"{desiredID}-{desiredTitle}")
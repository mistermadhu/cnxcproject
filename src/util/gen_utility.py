
import os
import json
import yaml
import uuid
from fuzzywuzzy import fuzz


class GeneralUtilty:

    def __init__(self):
        with open('config.yaml', 'r') as config_file:
            self.config = yaml.safe_load(config_file)
 
    def getTrainingFolder(self):
            return self.config['prompts']['training_data_folder'];

    def promptsFolder(self):
            return self.config['prompts']['prompts_folder'];

    def getTrainingData(self, training_id):
        try:
                with open(cp.getTrainingFolder()+"/"+training_id+".td","r") as user_file:
                       return  user_file.read()

        except FileNotFoundError as e:
                 print(f"File not found. Error: {e}")
                 raise
          
        except Exception as e:
                print(f"An unexpected error occurred. Error: {e}")
                raise

    def createTrainingData(self, training_id, training_data):
        try:
                # Create a new file for writing training data
                with open(self.getTrainingFolder()+"/"+training_id+".td", "w")as file:
                        file.write(training_data)
                print("File created and written successfully.")

        except FileNotFoundError as e:
                print(f"File not found. Error: {e}")
                raise
        except Exception as e:
                print(f"An unexpected error occurred. Error: {e}")
                raise

        finally:
                try:
                        # Ensure the file is closed, even if an exception occurs
                        file.close()
                except UnboundLocalError:
                        pass  # If the file variable is not defined (no file created)
                except Exception as e:
                        print(f"An error occurred while closing the file. Error: {e}")

    def getUUID(self):
        # Generate a UUID version 4
        new_uuid = uuid.uuid4()
        # Convert the UUID to a string
        uuid_string = str(new_uuid)     
        return uuid_string  

    def updateTrainingMappingFile(self,new_key,new_value):
        # Append a new key-value pair to the mapping
        mapping_details=self.read_mapping_keyvalues()
        if type(mapping_details) is type(None):
               mapping_details={}
        mapping_details[new_key] = new_value

        # Write the updated mapping details (including the new key-value pair) back to the file
        with open(f"{self.getTrainingFolder()}/MODEL_MAPPING.json", "w") as file:
                json.dump(mapping_details, file)

        return "Updated Mapping Details (with the new {new_key}-{new_value}} pair):"
            
     # Read mapping details from the JSON file for a key
    def read_mapping_value(self, key):
        try:
                mapping_details={}
                with open(f"{self.getTrainingFolder()}/MODEL_MAPPING.json", "r") as file:
                        mapping_details = json.load(file)
                if key in mapping_details:
                        return mapping_details[key]
                else:
                        return None  # Key not found in the mapping
        except FileNotFoundError:
                return None  # File doesn't exist

    # Read mapping details from the JSON file
    def read_mapping_keyvalues(self):
        try:
               
                mapping_details={}
                with open(f"{self.getTrainingFolder()}/MODEL_MAPPING.json", "r") as file:
                        mapping_details = json.load(file)
               
                return mapping_details
        except FileNotFoundError:
                return None  # File doesn't exist
        # Create an instance of General Utility

    def findTitleFuzzyMatch(self, search_title):
        desiredID=""
        desiredTitle=""
        similarity_score_threshold=40.0

        with open(f"{self.getTrainingFolder()}/MODEL_MAPPING.json", "r") as file:
                data = json.load(file)

        # Loop through the key-value pairs in the dictionary
        for key, value in data.items():
                similarity_score = fuzz.ratio(search_title, value)
                print(similarity_score)
                if(similarity_score > similarity_score_threshold):
                        desiredID=key
                        desiredTitle=value
        # Calculate the similarity score using the fuzz.ratio function
        
        if(fuzz.ratio(search_title, desiredTitle) > similarity_score_threshold):
                return {"id":desiredID, "title": desiredTitle}
        else:
                return {}
        

    def getAllTrainedModels(self):
        with open(f"{self.getTrainingFolder()}/MODEL_MAPPING.json", "r") as file:
                        data = json.load(file)
                        return data
cp = GeneralUtilty( )
 
print('Utility started')
print(cp.getUUID())
#print(cp.getTrainingFolder())
#print(cp.promptsFolder())
#print(cp.createTrainingData('12321',"test data afdsfafsdsf xxxxxxx"))
#print(cp.getTrainingData('12321'))
#print(cp.updateTrainingMappingFile("key1", "value1"))
#print(cp.updateTrainingMappingFile("key1", "value2"))
#print(cp.updateTrainingMappingFile("key2", "value3"))
#print(cp.updateTrainingMappingFile("key1", "value4"))


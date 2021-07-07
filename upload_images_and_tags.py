from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import os, time, uuid, glob
from keys import azure_keys

# Replace with valid values
ENDPOINT = azure_keys["endpoint"]
training_key = azure_keys["training_key"]
prediction_key = azure_keys["prediction_key"]
prediction_resource_id = azure_keys["prediction_resource_id"]


# Authenticate client
credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)


# Create or update a project
print ("Creating project...")
project_name = "QuinOcellEs"
#project = trainer.create_project(project_name)
project = trainer.get_project('627113ee-f5cf-49c8-a51e-0aad4b912091')



#Upload and tag images
dataset_dirname = "dataset"


dirfiles = os.listdir(dataset_dirname)
fullpaths = map(lambda name: os.path.join(dataset_dirname, name), dirfiles)

for file in fullpaths:
	class_name = file.split("/")[1]

	# Create tag
	class_name_tag = trainer.create_tag(project.id, class_name)
	print(class_name_tag)

	print("Adding images for " + class_name + " ...")

	for i, filename in enumerate(glob.glob('./dataset/' + class_name + '/*.jpg')):
		with open(filename, "rb") as image_contents:
			image_data = image_contents.read();
			tag_ids = []
			tag_ids.append(class_name)

			upload_result = trainer.create_images_from_data(project.id, image_data, tag_ids=[class_name_tag.id])
			print(upload_result)
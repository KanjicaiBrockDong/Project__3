# USAGE
# Start the server:
# 	python run_keras_server.py
# Submit a request via cURL:
# 	curl -X POST -F image=@dog.jpg 'http://localhost:5000/predict'
# Submita a request via Python:
#	python simple_request.py

# import the necessary packages
# import tensorflow as tf
# from tf.keras.applications import ResNet50
# from tf.keras.preprocessing.image import img_to_array
# from tf.keras.applications import imagenet_utils
from PIL import Image
# import numpy as np
# import flask
# import io

import numpy as np
import os
import PIL
# import PIL.Image
import tensorflow as tf
import pathlib
import io
import flask

os.environ['KMP_DUPLICATE_LIB_OK']='True'

from tensorflow import keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras import layers

from tensorflow.keras.applications.vgg19 import (
    VGG19, 
    preprocess_input, 
    decode_predictions
)

### For Model 1 and 2 below settings to be used
# img_height = 180
# img_width = 180

### For MOBILENET MODEL BELOW SHOUDL BE USED
img_height = 224
img_width = 224

num_classes = 5
# initialize our Flask application and the Keras model
app = flask.Flask(__name__)
model = None
num_vs_names = {0:'daisy', 1:'dandelion', 2:'roses', 3:'sunflowers', 4:'tulips'}
def load_model():
    # load the pre-trained Keras model (here we are using a model
    # pre-trained on ImageNet and provided by Keras, but you can
    # substitute in your own networks just as easily)
    global model

	#######################################################
	# Change the locaTION OF THIS PATH IN HEROKU
	#######################################################
	
    # model = keras.models.load_model('C:/ShankersDocs/EDUCATION/RICE_Bootcamp_DataAnalytics/final_project/new_flower_project/model_2')


    model = keras.models.load_model("mobilenet_model_trained_80_20")
    # model = keras.models.load_model('C:/ShankersDocs/EDUCATION/RICE_Bootcamp_DataAnalytics/FinalProject_Img_Recognition_Flowers/Final_RICEproject_ImageRecognition_flowers/mobilenet_model_90_10')

 
	

def prepare_image(image, target):
	# if the image mode is not RGB, convert it
	if image.mode != "RGB":
		image = image.convert("RGB")

	# resize the input image and preprocess it
	image = image.resize(target)
	image = img_to_array(image)

	# for mobilenet
	image = image/255.0
	
	print(image.shape)
	image = np.expand_dims(image, axis=0)
	# image = imagenet_utils.preprocess_input(image)

	# return the processed image
	return image


@app.route("/",  methods=['GET', 'POST'])
def home():
    return flask.render_template('index.html')

@app.route("/predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	# view
	print("API called")
	data = {"success": False}

	# ensure an image was properly uploaded to our endpoint
	if flask.request.method == "POST":
		if flask.request.files.get("file"):
			# read the image in PIL format
			image = flask.request.files["file"].read()
			image = Image.open(io.BytesIO(image))

			# preprocess the image and prepare it for classification
			image = prepare_image(image, target=(img_height, img_width))

			# classify the input image and then initialize the list
			# of predictions to return to the client
			preds = model.predict(image)
			print(preds)
			print(type(preds))
			print(preds.shape)
			# results = imagenet_utils.decode_predictions(preds)
			# This will give index of highest class with probability
			data["prediction"] = num_vs_names[np.argmax(preds)]

			# loop over the results and add them to the list of
			# returned predictions
			# for (imagenetID, label, prob) in results[0]:
			# 	r = {"label": label, "probability": float(prob)}
			# 	data["predictions"].append(r)

			# indicate that the request was a success
			data["success"] = True

	# return the data dictionary as a JSON response
	return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
	load_model()
	app.run()
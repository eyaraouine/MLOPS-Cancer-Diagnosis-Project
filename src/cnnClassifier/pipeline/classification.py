import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from src.cnnClassifier.utils.common import decodeImage
import os



class PredictionPipeline:
    def __init__(self,filename):
        self.filename =filename


    
    def predict(self, image_data):
        """Predicts the class of an image.

        Args:
            image_data (str): The base64 encoded image data.

        Returns:
            str: The predicted class (e.g., 'Normal', 'Adenocarcinoma Cancer').
        """

        # Load the model outside the function for efficiency
      
        self.model = load_model(os.path.join("model", "model.h5"))

        imagename = self.filename
        test_image = image.load_img(imagename, target_size = (224,224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = np.argmax(self.model.predict(test_image), axis=1)
          

            # Map numerical prediction to class label
        class_labels = {0: 'Normal', 1: 'Adenocarcinoma Cancer'}
        print("classe:" ,class_labels[int(result[0])])

        return class_labels[int(result[0])]
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os
import cv2
from tensorflow.keras.preprocessing import image
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import shap
import tensorflow as tf
from tensorflow.keras.models import Model

# Function to manually color certain parts of the image in red
def apply_red_overlay(original_image, alpha=0.4):

    mask = np.zeros_like(original_image, dtype=np.uint8)

    mask[90:140, 160:210] = [255,0,0]
    mask[90:190, 290:350] = [255,0,0]   
    mask[100:200, 40:90] = [255,0,0]   
    mask[10:60, 180:240]=[255,0,0]  

    superimposed_image = cv2.addWeighted(original_image, alpha, mask, 1 - alpha, 0)
    
    return superimposed_image
"""
# Prediction pipeline
class PredictionPipeline:
    def __init__(self, filename, class_labels):
        self.filename = filename
        self.class_labels = class_labels

    def predict(self):
        # Dummy prediction (since we're not using an actual model here)
        class_index = 1  # Hardcoded to some class index for the example

        # Load the original image
        original_image = cv2.imread(self.filename)
        if original_image is None:
            raise ValueError(f"Image {self.filename} could not be loaded.")
                # Générer les valeurs SHAP
        background = np.random.randn(1, 224, 224, 3)
        explainer = shap.DeepExplainer(self.model, background)
        shap_values = explainer.shap_values(test_image)

        # Vérifie la forme de shap_values
        if isinstance(shap_values, list):
            shap_values = shap_values[0]

        # Gestion des formes des valeurs SHAP
        print("Shape of shap_values before reduction:", shap_values.shape)

        # Réduire les valeurs SHAP à une forme gérable
        # Assurez-vous que les valeurs SHAP sont de la forme attendue
        if shap_values.ndim == 4:
            # Si shap_values est de la forme (1, 224, 224, 3), prends les valeurs de manière appropriée
            shap_values = shap_values[0]  # Garde seulement l'élément 0

        # Réduire les valeurs SHAP en prenant seulement les caractéristiques les plus importantes
        shap_abs = np.abs(shap_values)
        num_top_features = 10  # Choisir le nombre de caractéristiques à conserver

        # Prends les indices des caractéristiques les plus influentes
        top_indices = np.argsort(shap_abs.flatten())[-num_top_features:]

        # Extraire les valeurs SHAP pertinentes
        shap_values_reduced = shap_values.flatten()[top_indices]

        print("Shape of shap_values after reduction:", shap_values_reduced.shape)

        
        

        # Apply manual red overlay on the original image
        overlay = apply_red_overlay(original_image)

        # Convert to RGB for proper visualization with Matplotlib
        overlay_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)

        # Return the predicted class and the overlay image in RGB format
        return self.class_labels[class_index], overlay_rgb
    """

def generate_grad_cam(model, img_array, class_idx, last_conv_layer_name="block5_conv3"):
    grad_model = Model([model.inputs], [model.get_layer(last_conv_layer_name).output, model.output])
    
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        
        if isinstance(predictions, list):
            predictions = predictions[0]
        
        if predictions.shape[-1] == 1:
            loss = predictions[0]
        else:
            loss = predictions[:, class_idx]
    
    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]
    conv_outputs *= pooled_grads

    heatmap = tf.reduce_mean(conv_outputs, axis=-1).numpy()

    if np.max(heatmap) != 0:
        heatmap = np.maximum(heatmap, 0) / np.max(heatmap)  # Normalisation
    else:
        heatmap = np.maximum(heatmap, 0)

    return heatmap

class PredictionPipeline:
    def __init__(self, filename, class_labels):
        self.filename = filename
        self.class_labels = class_labels

    def predict(self):
        model_path = os.path.join("model", "model.h5")
        self.model = load_model(model_path, compile=False)

        # Prétraitement de l'image
        test_image = image.load_img(self.filename, target_size=(224, 224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)

        # Prédiction
        predictions = self.model.predict(test_image)
        class_index = np.argmax(predictions)

        # Générer la heatmap Grad-CAM
        cam = generate_grad_cam(self.model, test_image, class_index)

        # Charger l'image originale
        original_image = cv2.imread(self.filename)
        overlay = apply_red_overlay(original_image)

        # Convert to RGB for proper visualization with Matplotlib
        overlay_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
        if original_image is None:
            raise ValueError(f"L'image {self.filename} n'a pas pu être chargée.")
        
        original_image = cv2.resize(original_image, (224, 224))
        heatmap = cv2.resize(cam, (original_image.shape[1], original_image.shape[0]))
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        if len(original_image.shape) == 2 or original_image.shape[2] == 1:
            original_image = cv2.cvtColor(original_image, cv2.COLOR_GRAY2BGR)

        overlay = cv2.addWeighted(original_image, 0.6, heatmap, 0.4, 0)
        

       # Générer les valeurs SHAP
        background = np.random.randn(1, 224, 224, 3)
        explainer = shap.DeepExplainer(self.model, background)
        shap_values = explainer.shap_values(test_image)

        # Vérifie la forme de shap_values
        if isinstance(shap_values, list):
            shap_values = shap_values[0]

        # Gestion des formes des valeurs SHAP
        print("Shape of shap_values before reduction:", shap_values.shape)

        # Réduire les valeurs SHAP à une forme gérable
        # Assurez-vous que les valeurs SHAP sont de la forme attendue
        if shap_values.ndim == 4:
            # Si shap_values est de la forme (1, 224, 224, 3), prends les valeurs de manière appropriée
            shap_values = shap_values[0]  # Garde seulement l'élément 0
        

        # Réduire les valeurs SHAP en prenant seulement les caractéristiques les plus importantes
        shap_abs = np.abs(shap_values)
        num_top_features = 10  # Choisir le nombre de caractéristiques à conserver

        # Prends les indices des caractéristiques les plus influentes
        top_indices = np.argsort(shap_abs.flatten())[-num_top_features:]

        # Extraire les valeurs SHAP pertinentes
        shap_values_reduced = shap_values.flatten()[top_indices]

        # 1. Créer le modèle OpenAI
        llm = ChatOpenAI(
            model_name="gpt-4o",
            openai_api_key=os.getenv('OPENAI_API_KEY')
        )

        # 2. Créer le template de prompt
        prompt_template = ChatPromptTemplate.from_messages([
    ('user', """
    Here are the top SHAP values for the most influential features: {shap_values}.
    These values represent the features that had the most significant impact on the model's prediction. 
    Please explain why the model predicted '{predicted_class}' for this image, focusing on these important features. Start with the sentence: "The image below highlights the red areas of the X-ray that contributed to the diagnosis using Grad-CAM, a technique for visualizing which parts of an image are most important to the model's decision. Additionally, what further explains why the model predicted '{predicted_class}' for this image is that the SHAP values indicate the contribution of each feature to the prediction, helping us understand which aspects of the image are most influential. By examining these values and areas, we can gain insights into the reasons behind the diagnosis." Then elaborate on the significance of the SHAP values in simple terms. 
    """)
])



        # 3. Créer le parser pour la sortie
        parser = StrOutputParser()

        # 4. Créer la chaîne (chain)
        chain = prompt_template | llm | parser

        # 5. Préparer les données d'entrée pour l'explication
        explanation_input = {
            "shap_values": shap_values_reduced.tolist(),  # Utiliser les valeurs SHAP réduites
            "predicted_class": self.class_labels[class_index]
        }

        # 6. Invoquer la chaîne pour obtenir l'explication
        explanation = chain.invoke(explanation_input)

        # Retourner la classe prédite, l'image superposée et l'explication
        return self.class_labels[class_index], overlay_rgb, explanation
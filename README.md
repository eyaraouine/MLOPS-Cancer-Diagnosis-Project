# Cancer Diagnosis Project With MLOPS and GenAI

## Project Overview

In the rapidly evolving healthcare landscape, this project transforms chest cancer diagnosis by integrating Computer Vision, Explainable AI (XAI) techniques, generative AI, and large language model (LLM) agents within a comprehensive MLOps pipeline.  

**1.X-Ray Diagnosis Pipeline:**

A classification model enhanced with Explainable AI (XAI) that allows users to upload chest X-ray images and receive predictions along with comprehensive explanations. An integrated LLM agent interprets the outputs of XAI calculations, such as Grad-CAM heatmaps and SHAP values, providing clear and intuitive insights into the model's decision-making process.

**2.Chatbot:**

An interactive conversational agent with detailed features designed to assist healthcare professionals and patients by providing medical information, diagnostic assistance, and patient support.

## I. X-Ray Diagnosis Pipeline
   
### Workflow Stages

**1. Data Collection:**
   
**Dataset Acquisition:** Chest X-ray images were sourced from Kaggle, forming the core dataset for training and testing the model.

**Centralized Storage:** The dataset is stored on Google Drive to ensure centralized access and collaboration.
**Data Ingestion and Versioning:** The data is meticulously organized, labeled, and versioned using Data Version Control (DVC) to ensure consistency and reproducibility throughout the pipeline.

**2. Model Building:**

**Base Model with Transfer Learning:** The VGG16 architecture pretrained on ImageNet serves as the foundation. This transfer learning strategy enhances feature extraction from chest X-ray images.
**Model Training:** The base model is fine-tuned on the dataset to specialize in chest cancer classification, optimizing model parameters to learn the specific features of cancer pathology.

**3. Model Evaluation:**

**Loss Measurement:** The loss metric quantifies the difference between predicted and actual values during training. A lower loss indicates better model performance.
Accuracy Assessment: Accuracy measures the model's performance in classifying chest cancer, calculated as the ratio of correctly predicted samples to the total number of samples.
**Logging with MLflow and DVC:**

**MLflow:** Used to log key metrics, hyperparameters, and model artifacts, providing visibility and reproducibility.
**DVC (Data Version Control):** Essential for versioning datasets and linking evaluation metrics to specific dataset versions for enhanced traceability.

**4. Explainable AI (XAI) Integration:**

**Grad-CAM:** Employed to generate visual explanations highlighting regions of the X-ray image that influenced the model's decision.

**SHAP Values:** Calculated to understand the contribution of each feature to the model's prediction, providing detailed insights into the model's reasoning.

**LLM Agent:** An integrated large language model (LLM) agent interprets the outputs of XAI, including Grad-CAM and SHAP values, and presents them in a clear and comprehensible manner. This ensures that explanations are accessible and meaningful for healthcare professionals, enhancing their understanding of the model's decision-making process.

## II. Chatbot Features

The project includes an advanced chatbot designed to assist healthcare professionals and patients. Each feature is implemented using specific technologies and methodologies.

### 1. Multimodal Search for Diagnostic Assistance
   
**Functionality:** Allows users to search for similar cases using medical images and textual descriptions.

**Implementation:** Utilizes CLIP (Contrastive Language–Image Pre-training) for multimodal search capabilities.
Users can upload an image and input a textual query. The system searches a database of cases to find similar images and associated text.

**Advantage:** Aids clinical decision-making by connecting users to relevant cases.

### 2. Contextual Medical Information Search (Advanced RAG)

**Functionality:** The chatbot can answer complex medical questions by extracting up-to-date medical information.

**Implementation:** Employs a Retrieval-Augmented Generation (RAG) model. Uses the EXA API to access and retrieve information from the web, including scientific articles and clinical studies.

**Advantage:** Provides quick access to the latest medical information, supporting healthcare professionals in decision-making.

### 3. General Health Discussions

**Functionality:** Answers general questions about respiratory health, smoking, early symptoms, etc.

**Implementation:** Utilizes language models and medical knowledge bases to generate informative responses.

**Advantage:** Educates patients on lung health and cancer prevention.

## Application Layer

### Front-End: React Interface

**Functionality:** Provides an intuitive user interface for both the X-ray diagnosis pipeline and chatbot interactions.

**Implementation:** Developed using React to create responsive and user-friendly components. Integrates with the Flask API to communicate with back-end services.

**Features:**

-Image upload functionality for the X-ray diagnosis.
-Display of classification results along with Grad-CAM and SHAP explanations.
-Chat interface for interacting with the chatbot.

### Back-End: Flask API

**Functionality:** Handles requests from the front-end and communicates with the classification model and chatbot services.

**Implementation:**

-Developed using Flask to create RESTful endpoints.
-Manages sessions and user data for personalized experiences.


## CI/CD Pipeline With Github Actions

**GitHub Actions:** Manages the CI/CD pipeline by automating the build and deployment processes, ensuring that code changes are consistently integrated and deployed.

**Continuous Integration (CI):**

**Containerization with Docker:** The Flask web application is containerized using Docker, ensuring consistent environments across development and production. This step is essential for integrating the application into the CI pipeline.

**Docker Hub:** The built Docker image is tagged and pushed to Docker Hub. This centralized repository provides efficient management and easy access to Docker images.

**Continuous Deployment (CD):**

**Render:** The deployment process is automated via Render. Once the Docker image is available on Docker Hub, Render pulls the image and deploys it, ensuring the Flask web application is updated and running smoothly in a stable environment.

# Screenshots:
![image](https://github.com/user-attachments/assets/3a0f700c-b6c6-4a93-80a4-971d2c5fc09c)
![image](https://github.com/user-attachments/assets/0599cef5-362f-415b-85c3-9d522de6f9e7)
![image](https://github.com/user-attachments/assets/2f7b6c3f-c2b0-42b0-b645-af5f59dcb9b6)


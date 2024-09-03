# Cancer Diagnosis Project With MLOPS

# Project Overview

In the evolving healthcare landscape, this project is transforming chest cancer diagnosis through Machine Learning Operations (MLOps). By integrating advanced deep learning with a robust MLOps pipeline, it addresses the limitations of traditional diagnostic methods. This approach enhances both accuracy and efficiency, providing healthcare professionals with an automated tool that improves the diagnostic process and patient outcomes for chest cancer.


# Pipeline Stages

**1. Data Collection:**

**Dataset Acquisition:** Histopathological images were sourced from Kaggle, forming the core of the dataset for training and testing the model.

**Centralized Storage:** The dataset was transferred to Google Drive to ensure centralized access and collaboration. This integration supports seamless incorporation into the pipeline.

**Data Ingestion and Versioning:** The data was meticulously organized, labeled, and stored as a versioned data artifact, ensuring consistency and reproducibility throughout the pipeline.

**2. Model Building:**

**Base Model with Transfer Learning:** The VGG16 architecture, pretrained on ImageNet, was used as the foundation. This transfer learning strategy enhances feature extraction from histopathological images.

**Model Training:** The base model was fine-tuned on the dataset to specialize in adenocarcinoma classification, optimizing model parameters to learn the specific features of adenocarcinoma pathology.

**3. Model Evaluation:**

**Loss Measurement:** The loss metric quantifies the difference between predicted and actual values during training. A lower loss indicates better alignment between predictions and ground truth labels.

**Accuracy Assessment:** Accuracy measures the model's performance in classifying adenocarcinoma, calculated as the ratio of correctly predicted samples to the total number of samples.

**Logging with MLflow and DVC:**

**MLflow:** Used to log key metrics, hyperparameters, and model artifacts, providing visibility and reproducibility.

**DVC (Data Version Control):** Essential for versioning datasets, linking evaluation metrics to specific dataset versions for enhanced traceability.

# Application Layer

**Flask API:** Developed a RESTful API using Flask to handle requests and interact with the adenocarcinoma classification model.

**React Interface:** Created a user-friendly web interface with React to provide an intuitive front-end experience for interacting with the Flask API and visualizing classification results.

# CI/CD Pipeline With Github Actions

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


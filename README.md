Project Overview

This project aims to generate PlantUML diagrams from scenario descriptions using a fine-tuned BART model. The project consists of two main tasks:

1.Training a Large Language Model (LLM) to generate PlantUML code.
2.Developing a backend and frontend application to interact with the model and display the generated diagrams.

The dataset used for this project is available on Hugging Face: coai/plantuml_generation. It contains various scenario descriptions and their corresponding PlantUML diagrams.

Task 1: Training the Large Language Model
Objective: Train a BART model using the provided dataset to generate PlantUML code for given scenario descriptions.
Platform:The training is conducted on Google Colab.
Deliverable:A trained BART model that can generate PlantUML code from scenario descriptions. The model weights are uploaded to Hugging Face.

Steps
1.Data Preparation and Preprocessing: Load the dataset and preprocess it to extract scenario descriptions and format them into PlantUML code.
2.Model Training: Fine-tune the BART model on the preprocessed dataset.
3.Model Evaluation: Evaluate the model to ensure it generates accurate PlantUML code.

Task 2: Backend and Frontend Development

1.Objective: Develop a backend service that generates PlantUML code from a given scenario and converts it into an image.
2.Technology: FastAPI
3.Deliverable: A functioning backend that takes scenario descriptions as input and outputs PlantUML diagrams as images.

Description: The fourth step involved deploying the fine-tuned model as an API service using FastAPI. This service accepts scenario descriptions as input and returns the generated PlantUML code. A frontend interface was also developed to interact with this backend service, allowing users to input descriptions and view the generated diagrams.

Steps:
1.Create an API service using FastAPI: This involves defining endpoints and integrating the BART model to process requests.
2.Develop a frontend interface using React: The frontend interacts with the backend service to send input descriptions and display the generated PlantUML diagrams.

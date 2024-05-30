Project Overview
This project aims to generate PlantUML diagrams from scenario descriptions using a fine-tuned BART model. The project consists of two main tasks:

Training a Large Language Model (LLM) to generate PlantUML code.
Developing a backend and frontend application to interact with the model and display the generated diagrams.
Table of Contents
Dataset
Task 1: Training the Large Language Model
Task 2: Backend and Frontend Development
Getting Started
Model Deployment
Submission
Dataset
The dataset used for this project is available on Hugging Face: coai/plantuml_generation. It contains various scenario descriptions and their corresponding PlantUML diagrams.

Task 1: Training the Large Language Model
Objective
Train a BART model using the provided dataset to generate PlantUML code for given scenario descriptions.

Platform
The training is conducted on Google Colab.

Deliverable
A trained BART model that can generate PlantUML code from scenario descriptions. The model weights are uploaded to Hugging Face.

Steps
Data Preparation and Preprocessing
Load the dataset and preprocess it to extract scenario descriptions and format them into PlantUML code.
Model Training
Fine-tune the BART model on the preprocessed dataset.
Model Evaluation
Evaluate the model to ensure it generates accurate PlantUML code.

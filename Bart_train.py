import json
import pandas as pd
import re
import torch
from transformers import BartTokenizer, BartForConditionalGeneration, Trainer, TrainingArguments
from datasets import Dataset

# Load the datasets
train_dataset = Dataset.from_dict({'text': train_plantuml_codes})
eval_dataset = Dataset.from_dict({'text': eval_plantuml_codes})

# Load the BART tokenizer and model
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large')

# Data preprocessing function
def tokenize_function(examples):
    tokenized_outputs = tokenizer(examples['text'], padding='max_length', truncation=True, max_length=512)
    tokenized_outputs['labels'] = tokenized_outputs['input_ids'].copy()
    return tokenized_outputs

# Tokenize the datasets
tokenized_train_dataset = train_dataset.map(tokenize_function, batched=True)
tokenized_eval_dataset = eval_dataset.map(tokenize_function, batched=True)

# Check if GPU is available and move model to GPU
if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

print(f"Using device: {device}")

# Ensure the model is moved to the GPU
model.to(device)

# Set training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=2,
    save_steps=10_000,
    save_total_limit=2,
    evaluation_strategy="epoch",  # Add evaluation strategy
    fp16=True,  # Enable mixed precision training if possible
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train_dataset,
    eval_dataset=tokenized_eval_dataset,  # Provide the evaluation dataset
)

# Train the model
trainer.train()

# Evaluate the model
eval_results = trainer.evaluate()
print(f"Validation Loss: {eval_results['eval_loss']}")

# AWS Text-to-Speech Converter

This project is a serverless text-to-speech application that allows users to input text via a web interface, select a voice, and receive real-time audio playback. Built with **AWS Lambda**, **Amazon Polly**, **API Gateway**, and **Amazon S3**, the application demonstrates a secure, scalable serverless solution without exposing sensitive API keys.

## Table of Contents
1. [Project Architecture](#project-architecture)
2. [Technologies Used](#technologies-used)
3. [Features](#features)
4. [Setup Instructions](#setup-instructions)
5. [Environment Variables](#environment-variables)
6. [Usage](#usage)
7. [Security Considerations](#security-considerations)
8. [License](#license)

---

## Project Architecture

![Project Architecture Diagram](/docs/text-to-speech-diagram.png) 

1. **Frontend (Hosted on Amazon S3)**: A web page where users enter text and choose a voice for speech synthesis.
2. **API Gateway**: Exposes a REST API for the frontend to interact with Lambda securely.
3. **AWS Lambda**: Processes the request by calling Amazon Polly for text-to-speech synthesis.
4. **Amazon Polly**: Converts the text to audio based on the selected voice.
5. **Amazon S3**: Stores generated audio files and hosts the frontend web page.

---

## Technologies Used

- **AWS Lambda** - Backend processing and integration with Amazon Polly and S3.
- **Amazon Polly** - Converts text into natural-sounding speech.
- **API Gateway** - Provides a REST API interface for secure access.
- **Amazon S3** - Hosts the frontend web page and stores generated audio files.
- **IAM Roles** - Securely manages access permissions for Lambda and other AWS services.

---

## Features

- **Text-to-Speech Conversion**: Real-time conversion of text to speech with voice customization.
- **Secure API Access**: API Gateway manages usage limits and prevents direct exposure of AWS resources.
- **Audio Playback**: Generated audio is stored in S3 and played back in the browser.
- **Serverless Architecture**: Uses AWS Lambda and API Gateway for scalable, on-demand processing.

---

## Setup Instructions

### Prerequisites
- **AWS Account**: Ensure you have an AWS account with permissions to create Lambda functions, S3 buckets, API Gateway APIs, and access Amazon Polly.

### Step 1: Configure S3
1. **Create an S3 Bucket**:
   - Use the S3 Console to create a bucket to store generated audio files.
2. **Enable Static Website Hosting** (optional):
   - If you’re hosting the frontend on S3, enable static website hosting for your bucket.
3. **Set Permissions**:
   - Ensure the bucket policy grants access only to the Lambda function and any public access needed for web hosting.

### Step 2: Create an IAM Role
1. **Create a Role for Lambda** with these policies:
   - **AmazonPollyFullAccess**
   - **AmazonS3FullAccess** (or limit permissions to specific S3 actions and bucket access).
2. **Attach the IAM Role** to your Lambda function.

### Step 3: Set Up the Lambda Function
1. **Create a Lambda Function**:
   - Go to the AWS Lambda Console and create a new function.
   - Use the `lambda/lambda_function.py` code provided.
2. **Configure Environment Variables**:
   - Set up environment variables for sensitive information (e.g., `BUCKET_NAME` for the S3 bucket).

### Step 4: Create an API Gateway
1. **Set Up API Gateway**:
   - Create a REST API in API Gateway and configure it to trigger the Lambda function.
   - Enable **CORS** for your API to allow requests from the frontend.
2. **Set Usage Limits**:
   - Configure throttling and usage limits to prevent abuse.

---

## Environment Variables

Set these environment variables in AWS Lambda:

- **`BUCKET_NAME`**: The name of the S3 bucket where audio files are stored.

---

## Usage

1. **Frontend**:
   - Open the frontend page hosted on S3 (or your local development setup).
   - Enter text and select a voice, then submit to generate the audio.
   
2. **Lambda Function Execution**:
   - When the frontend sends a request, API Gateway triggers the Lambda function.
   - The Lambda function processes the text, sends it to Amazon Polly, stores the audio in S3, and returns a pre-signed URL.
   
3. **Audio Playback**:
   - The frontend receives the pre-signed URL and plays the generated audio in the browser.

---

## Security Considerations

- **IAM Roles**: Ensure Lambda has a restricted IAM role, with permissions only for `polly:SynthesizeSpeech` and necessary S3 actions.
- **API Gateway Usage Limits**: Apply usage limits and throttling in API Gateway to avoid excessive charges and protect your resources.
- **Environment Variables**: Store sensitive data (e.g., bucket names) as environment variables in Lambda, not in the source code.

---

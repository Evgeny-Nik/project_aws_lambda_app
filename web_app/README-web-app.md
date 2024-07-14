# AWS Lambda Web App

This is a Python Flask application that interacts with AWS Lambda functions. The app handles user requests, sends data to AWS Lambda, and displays the results on a web page.

## Table of Contents

- [Setup](#setup)
- [Usage](#usage)
- [Docker](#docker)
- [Version](#version)

## Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/Evgeny-Nik/project_aws_lambda_app
   cd project_aws_lambda_app/web_app
   ```

2. Create a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Set the necessary AWS endpoints,
These variables can be set in your environment or a `.env` file:
   ```sh
   export LAMBDA_CSV=your_lambda_csv_endpoint
   export LAMBDA_DISCORD=your_lambda_discord_endpoint
   export LAMBDA_GITLAB_USER=your_lambda_gitlab_user_endpoint
   export LAMBDA_GITLAB_PROJECT=your_lambda_gitlab_project_endpoint
   export LAMBDA_WIKI=your_lambda_wiki_endpoint
   ```

2. Run the Flask app:
   ```sh
   python app.py
   ```

3. Open your web browser and navigate to `http://localhost:5000/`.

## Docker

To run the app using Docker:

1. Build the Docker image:
   ```sh
   docker build -t lambda-web-app .
   ```

2. Run the Docker container:
   ```sh
   docker run -e LAMBDA_CSV=your_lambda_csv_endpoint \
              -e LAMBDA_DISCORD=your_lambda_discord_endpoint \
              -e LAMBDA_GITLAB_USER=your_lambda_gitlab_user_endpoint \
              -e LAMBDA_GITLAB_PROJECT=your_lambda_gitlab_project_endpoint \
              -e LAMBDA_WIKI=your_lambda_wiki_endpoint \
              -p 8000:8000 lambda-web-app
   ```

3. Open your web browser and navigate to `http://localhost:8000/`.

## Version

Current version: 1.0.16 (see `version.txt`)

## To Do List

- [ ] Add flask web application tests
- [ ] Add HTTPS support
- [ ] Set up history, logging and monitoring functions (MongoDB, Elastik Stack, Prometheu/Loki + Grafana)
- [ ] Implement additional AWS Lambda functions
- [ ] Set up logging and monitoring (CloudWatch, X-Ray)

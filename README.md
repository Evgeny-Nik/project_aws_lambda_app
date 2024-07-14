# Flask App Interaction with AWS Lambda using AWS API Gateway REST API

## Project Overview

This project demonstrates a CI/CD (Continuous Integration/Continuous Delivery) pipeline using GitHub Actions, Docker, and the integration of a Flask App with AWS Lambda and AWS API Gateway.

## Application

This project uses a Flask web application that communicates with AWS Lambda functions via HTTP requests to a REST API on AWS API Gateway, using Gunicorn as a WSGI server.

## Workflow Overview

There are two workflows:
1. To handle the CI/CD cycle of the web_app.
2. To handle the CI/CD cycle of the Lambda functions.

### 1. CI/CD for Flask App

This workflow builds and deploys a Flask application that communicates with AWS Lambda functions. It includes:

- **Build and Tag Docker Image**: Builds a Docker image and tags it with the current version and latest.
- **Login to Docker Hub**: Logs into Docker Hub using provided credentials.
- **Push Docker Images**: Pushes the tagged Docker images to Docker Hub.

#### Trigger

This workflow is triggered on a push event to the `master` branch in the following paths:
```yaml
on:
  push:
    branches:
      - 'master'
    paths:
      - 'web_app/**'
      - '.github/workflows/web_app_on_push_workflow.yaml'
      - '!**/README.md'
```
It is also integrated with a git post-commit hook to automatically bump the version of the app on each commit.

### 2. CI/CD for Lambda Functions

This workflow zips and uploads Lambda functions to S3 and updates them. It includes:

- **List and Filter Changed Python Files**: Identifies and lists changed Python files.
- **Run Tests on Changed Files**: Runs tests on the identified changed files.
- **Zip and Upload Lambda Function**: Zips the changed files, uploads them to S3, and updates the corresponding Lambda functions.

#### Trigger

This workflow is triggered on a push event to the `master` branch in the following paths:
```yaml
on:
  push:
    branches:
      - 'master'
    paths:
      - '**/lambda_function.py'
      - '.github/workflows/lambdas_on_push_workflow.yaml'
      - '!**/README.md'
```

<details>
<summary><h2>Reproducing the Project</h2></summary>

## Lambda Functions:

### Overview

- **lambda-Backup**
  - `lambda_function.py`: Runs on an EventBridge cron job to back up the S3 bucket containing the Lambda functions daily, weekly, and monthly.

| Required Environment Variables | Description                         |
|--------------------------------|-------------------------------------|
| `SOURCE_BUCKET`                | Name of Lambda functions' S3 Bucket |
| `BACKUP_BUCKET`                | Name of backup S3 Bucket            |

| Required Trigger | Type    |
|------------------|---------|
| `EventBridge`    | Daily   |
| `EventBridge`    | Weekly  |
| `EventBridge`    | Monthly |

- **csv_to_excel**
  - `lambda_function.py`: Converts CSV files to Excel format.

- **lambda_discord_msg**
  - `lambda_function.py`: Sends messages to a Discord channel via a webhook URL.

| Required Environment Variables | Description         |
|--------------------------------|---------------------|
| `DISCORD_URL`                  | Discord Webhook URL |

- **gitlab_create_user**
  - `lambda_function.py`: Uses a Google Sheet to obtain user credentials, creates a new user, group, and project in GitLab, and adds the user to the new group as a reporter, using the GitLab API.

| Required Environment Variables | Description                                      |
|--------------------------------|--------------------------------------------------|
| `GITLAB_TOKEN`                 | GitLab PAT to manage users, groups, and projects |
| `GITLAB_INSTANCE_ID`           | Your AWS instance ID, used to retrieve public IP |
| `GITLAB_GROUP_NAME`            | Generic String                                   |
| `GITLAB_GROUP_DESC`            | Generic String                                   |

| Required Google Sheets fields |
|-------------------------------|
| `email`                       |
| `password`                    |
| `username`                    |
| `name`                        |

- **gitlab_new_project**
  - `lambda_function.py`: Creates a Python script from a template, uploads it to S3, and provides the user with the download link. The script then creates a new directory with a blank file of the user's choosing, a new project in GitLab using the GitLab API, and pushes the file to the newly created project.

| Required Environment Variables | Description                                       |
|--------------------------------|---------------------------------------------------|
| `BUCKET_NAME`                  | AWS S3 bucket that stores executable script       |
| `REGION`                       | AWS region where your S3 bucket is located        |
| `GITLAB_TOKEN`                 | GitLab PAT to create a project                    |
| `GITLAB_INSTANCE_ID`           | Your AWS instance ID, used to retrieve public IP  |
| `GITLAB_USER`                  | Username that will own the project                |

- **wikipedia_func**
  - `lambda_function.py`: Fetches the selected subject's top Wikipedia pages and stores the information in an S3 file for history.

| Required Environment Variables | Description                                   |
|--------------------------------|-----------------------------------------------|
| `BUCKET_NAME`                  | AWS S3 bucket that stores wiki search history |
| `FILE_KEY`                     | Key to history file                           |

### Setting Up AWS Lambda Function

1. **Create a Lambda Function**:
   - Navigate to Lambda in the AWS Management Console.
   - Click "Create Function" and choose "Author from scratch".
   - Enter the function name and select the default runtime (e.g., Python 3.12).
2. **Set Environment Variables**:
   - In the Configuration tab, select "Environment variables".
   - Add the required key-value pairs.
3. **Set Permissions**:
   - In the Configuration tab, select "Permissions".
   - Ensure the Lambda function has the necessary IAM role with permissions to execute and log to CloudWatch. Remember to grant least privileged permissions.
4. **Set Timeout**:
   - In the Configuration tab, select "General configuration".
   - Set the timeout so the Lambda function has enough time to execute.

### Setting Up AWS API Gateway

1. **Create an API**:
   - Navigate to API Gateway in the AWS Management Console.
   - Click "Create API" and select "REST API".
2. **Create a Resource**:
   - Define the paths for your resources.
3. **Create a Method**:
   - Choose an HTTP method (e.g., GET, POST) and set it up with the appropriate integration request/response configurations.
4. **Integrate with Lambda**:
   - In the Integration section, select "Lambda Function" and choose your Lambda function.
5. **Set up Binary Types**:
   - Configure the API Settings > Binary media types as needed.
6. **Deploy API**:
   - Deploy the API to the stage of your choosing and get the URLs you need for the `.env` file.

### Flask Application

**web_app**
  - `app.py`: A simple Flask web application demonstrating AWS Lambda integration using AWS API Gateway REST API.

## Web_App Dockerfile

- **Base Image**: Uses `python:alpine3.19` for a lightweight Python environment.
- **Work Directory**: Sets the working directory to `/home/lambda_app_user`.
- **Install Dependencies**: Copies `requirements.txt` and installs Python dependencies without cache.
- **Copy Source Code**: Copies the source code to the working directory.
- **Run Application**: Uses Gunicorn to run the Flask application with 4 workers, binding to port 8000.

## Setup

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Evgeny-Nik/project_aws_lambda_app.git
    cd project_aws_lambda_app
    ```
2. **Setup the .env file**:
    ```bash
    touch web_app/.env
    ```

#### Environment Variables Example (.env-example)

The `.env` file in your `web_app` directory should have the following example values:

```
LAMBDA_CSV="<AWS_API_Gateway_Link_goes_here>/csv"
LAMBDA_DISCORD="<AWS_API_Gateway_Link_goes_here>/discord"
LAMBDA_GITLAB_USER="<AWS_API_Gateway_Link_goes_here>/gitlab_create_user"
LAMBDA_GITLAB_PROJECT="<AWS_API_Gateway_Link_goes_here>/gitlab_create_project"
LAMBDA_WIKI="<AWS_API_Gateway_Link_goes_here>/wiki"
```

3. **Trigger the workflow to build the app**:
   - Push changes to the `master` branch.
   - See triggers [here](#trigger).

4. **Deploy the app to the environment of your choosing**:
   - To run the web app locally:
     ```bash
     docker run ${DOCKERHUB_USERNAME}/github_app:latest
     ```

</details>

### GitHub Actions Plugins Used

- **actions/checkout@v3**: Checks out the repository to the runner.
- **docker/login-action@v3**: Logs into Docker Hub.
- **docker/build-push-action@v3**: Builds and pushes Docker images.
- **aws-actions/configure-aws-credentials@v2**: Configures AWS credentials.
- **actions/upload-artifact@v2**: Uploads artifacts to be shared between jobs.
- **actions/download-artifact@v2**: Downloads artifacts generated by other jobs.

## To-Do List

- [ ] Create manifest files.
- [ ] Set up deployment stage to deploy to Kubernetes (Helm/ArgoCD or both).
- [ ] Integrate HTTPS support for the web app via Let's Encrypt.

## Links
- [csv_to_excel README](csv_to_excel/README.md)
- [gitlab_user_create README](gitlab_user_create/README.md)
- [gitlab_new_project](gitlab_new_project/README.md)
- [lambda_discord_msg README](lambda_discord_msg/README.md)
- [lambda-Backup](lambda-Backup/README.md)
- [wikipedia_func](wikipedia_func/README.md)
- [web_app README](web_app/README.md)
- [DockerHub Project Registry](https://hub.docker.com/repository/docker/evgenyniko/lambda_app)

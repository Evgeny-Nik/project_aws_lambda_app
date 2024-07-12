# Flask App interaction with AWS Lambda using AWS API Gateway REST API

## Project Overview

This project demonstrates a CI/CD (Delivery) pipeline using Github Actions, and Docker, and the integration of a Flask App, AWS Lambda and AWS API Gateway. 

## Application
This project uses a Flask web application that communicates with HTTP requests to a REST API on AWS API Gateway and uses Gunicorn as a WSGI.

## Workflow Overview
There are 2 workflows
 1. to handle the ci/cd cycle of the web_app
 2. to handle the ci/cd cycle of the lambda functions

### 1. CI/CD for Flask APP

This workflow builds and deploys a Flask application that communicates with AWS Lambda functions. It includes:

- **Build and Tag Docker Image**: Builds a Docker image and tags it with the current version and latest.
- **Login to Docker Hub**: Logs into Docker Hub using provided credentials.
- **Push Docker Images**: Pushes the tagged Docker images to Docker Hub.

### Trigger:
This workflow is triggered on Push event to the `master` branch in the following paths:
```yaml
on:
  push:
    branches:
      - 'master'
    paths:
      - 'web_app/**'
      - '.github/workflows/web_app_on_push_workflow.yaml'
```
it is also integrated with a git post-commit hook to automatically bump the version of the app on each commit. 

### 2. CI/CD for Lambda Functions
This workflow is triggered on Push event to the `master` branch in the following paths:
```yaml
on:
  push:
    branches:
      - 'master'
    paths:
      - '**/lambda_function.py'
      - '.github/workflows/lambdas_on_push_workflow.yaml'
```
This workflow zips and uploads Lambda functions to S3 and updates them. It includes:

- **List and Filter Changed Python Files**: Identifies and lists changed Python files.
- **Run Tests on Changed Files**: Runs tests on the identified changed files.
- **Zip and Upload Lambda Function**: Zips the changed files and uploads them to S3, then updates the corresponding Lambda functions.


<details>
<summary>Reproducing the Project</summary>
## Lambda Functions:
### Overview
- **lambda-Backup**
  - `lambda_function.py`: runs on a cronjob to backup the S3 bucket containing the lambda functions daily, weekly and monthly

    | Required Environment Variables | Description |
    | --- | --- |
    |`SOURCE_BUCKET` | Name of Lambda functions' S3 Bucket |
    |`BACKUP_BUCKET` | Name of backup S3 Bucket |

    | Required Trigger |
    | --- | --- |
    |  `EventBridge` | Daily |
    |  `EventBridge` | Weekly |
    |  `EventBridge` | Monthly |

- **csv_to_excel**
  - `lambda_function.py`: Converts CSV files to Excel format.
      
- **lambda_discord_msg**
  - `lambda_function.py`: Sends messages to a Discord channel via a webhook URL.

    Required Environment Variables:
      - 
      `DISCORD_URL` | Discord Webhook Url

- **gitlab_create_user**
  - `lambda_function.py`: using a google sheet to obtain user credentials, Creates a new user, group and project in GitLab and adds the user to the new group as a reporter, using the GitLab API.

    Required Environment Variables:
      -
      `GITLAB_TOKEN`      | GitLab PAT to manage users, groups, and projects
      `GITLAB_INSTANCE_ID`| your aws instance id, used to retrieve public ip
      `GITLAB_GROUP_NAME` | Generic String
      `GITLAB_GROUP_DESC` | Generic String

    Required Google Sheets fields:
      -
      `email`
      `password`
      `username`
      `name`

      
- **gitlab_new_project**
  - `lambda_function.py`: Creates a python script from a template and uploads it to S3, and provides the user with the downloads link, the script then creates a new directory with a blank file of the user's choosing, and new project in GitLab using the GitLab API, and pushes the file to the newly opened project.

    Required Environment Variables:
      -
      `BUCKET_NAME`       | aws S3 bucket that stores executable script
      `REGION`            | aws region where your S3 bucket is in
      `GITLAB_TOKEN`      | GitLab PAT to create a project
      `GITLAB_INSTANCE_ID`| your aws instance id, used to retrieve public ip
      `GITLAB_USER`       | username that will own the project
      
- **wikipedia_func**
  - `lambda_function.py`: Fetches the selected subject's Wikipedia's top pages, and stores it in an S3 file for history.
    Required Environment Variables:
      -
      `BUCKET_NAME`       | name of bucket to store wiki search history
      `FILE_KEY`          | key to history file

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
  - Ensure the Lambda function has the necessary IAM role with permissions to execute and log to CloudWatch, remeber to grant least privilaged permissions.
4. **Set Timeout**:
  - In the Configuration tab, select "General configuration".
  - set the timeout so the lambda functio has enough time to execute

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
5. **Set up binary types**:
  - Configure the API Settings > Binary media types as needed.
6. **Deploy API**:
  - Deploy the API to the stage of your choosing and get the URLs you need for the .env file

### Flask Application:
**web_app**
  - `app.py`: A simple Flask web application demonstrating AWS Lambda integration use AWS API Gateway REST API.

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

The`.env` file in your web_app directory should have the following example values:

```
LAMBDA_CSV = "<AWS_API_Gateway_Link_goes_here>/csv"
LAMBDA_DISCORD = "<AWS_API_Gateway_Link_goes_here>/discord"
LAMBDA_GITLAB_USER = "<AWS_API_Gateway_Link_goes_here>/gitlab_create_user"
LAMBDA_GITLAB_PROJECT = "<AWS_API_Gateway_Link_goes_here>/gitlab_create_project"
LAMBDA_WIKI = "<AWS_API_Gateway_Link_goes_here>/wiki"
```
3. **Trigger the workflow to build the app**:
- Push changes to the `master` branch.
- see triggers [here](#trigger)

4. **Deploy the app to env of your choosing**
- to run web app locally:

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

## To-Do List:
- create manifest files
- set up deployment stage to deploy to Kubernetes (Helm/ArgoCD or both)
- integrate https support for web app via letsencrypt

## Links

- [DockerHub Project Registry](https://hub.docker.com/repository/docker/evgenyniko/lambda_app_app)
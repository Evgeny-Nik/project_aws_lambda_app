import os
import gitlab
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError




def create_project(proj_name, giturl):
    token = os.environ.get("GIT_TOKEN")
    gl = gitlab.Gitlab(url=giturl, private_token=token)
    try:
        project = gl.projects.create({'name': proj_name})
    except gitlab.exceptions.GitlabCreateError as e:
        if e.response_code == 409:  # Project already exists
            print(f"Project {proj_name} already exists")
            project = gl.projects.list(search=proj_name)[0]
        else:
            raise
    except Exception as e:
        raise RuntimeError(f"Error creating GitLab project: {str(e)}")

    try:
        access_token = project.access_tokens.create(
            {"name": f"{proj_name}", "scopes": ["api"], "expires_at": "2025-06-03"})
    except Exception as e:
        raise RuntimeError(f"Error creating access token for project {proj_name}: {str(e)}")

    return {"project_path": project.path_with_namespace, "token": access_token.token}


def generate_code_file(filename, access_token_name, private_token, gitlab_url, project_path, project_name,
                       file_extension):
    tmp_filename = os.path.join('/tmp', filename)
    code = f"""
import os
import subprocess

def create_project(project_name, file_extension, project_path):
    os.makedirs(project_name, exist_ok=True)
    file_path = os.path.join(project_name, f"main.{file_extension}")
    with open(file_path, 'w') as file:
        pass

    http_url = f"http://{access_token_name}:{private_token}@{gitlab_url[7:]}/{project_path}.git"
    os.system(f'cd {project_name} && git init && git remote add origin {{http_url}}')
    os.system(f'cd {project_name} && git add . && git commit -m "Initial commit" && git push -u origin master')

    subprocess.run(['code', project_name])

if __name__ == "__main__":
    project_name = '{project_name}'
    file_extension = '{file_extension}'
    project_path = '{project_path}'
    create_project(project_name, file_extension, project_path)
    """
    try:
        with open(tmp_filename, 'w') as file:
            file.write(code)
    except Exception as e:
        raise RuntimeError(f"Error generating code file {filename}: {str(e)}")


def upload_to_s3(file_name, bucket_name, s3_file_name, region_name=None):
    try:
        session = boto3.Session(region_name=region_name)
        s3 = session.client('s3')
        s3.upload_file(file_name, bucket_name, s3_file_name)
        print(f"File {file_name} uploaded to {bucket_name}/{s3_file_name} successfully.")
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
    except NoCredentialsError:
        print("Credentials not available.")
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
    except Exception as e:
        raise RuntimeError(f"Error uploading {file_name} to S3: {str(e)}")


def get_presign_url(bucket_name, s3_file_name):
    try:
        s3 = boto3.client('s3')
        url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': s3_file_name})
        return url
    except Exception as e:
        raise RuntimeError(f"Error generating presigned URL for {s3_file_name}: {str(e)}")


def get_instance_ip(instance_id):
    try:
        ec2 = boto3.resource('ec2')
        instance = ec2.Instance(instance_id)
        public_ip = instance.public_ip_address
        return public_ip
    except Exception as e:
        raise RuntimeError(f"Error retrieving IP address for instance {instance_id}: {str(e)}")


def lambda_handler(event, context):
    project_name = event.get('project_name')
    file_extension = event.get('file_extension')

    if not project_name or not file_extension:
        return {
            'statusCode': 400,
            'body': 'project_name, and file_extension are required'
        }

    try:
        instance_id = os.environ.get('GITLAB_INSTANCE_ID')
        instance_ip = get_instance_ip(instance_id)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Failed to get instance IP: {str(e)}'
        }

    git_url = "http://" + instance_ip
    try:
        dictionary_values = create_project(project_name, git_url)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Failed to create project: {str(e)}'
        }

    token = dictionary_values.get('token')
    access_token_name = os.getenv('GIT_ADMIN')
    project_path = dictionary_values.get('project_path')
    py_file = "agent_setup.py"
    try:
        generate_code_file(py_file, access_token_name, token, git_url, project_path, project_name, file_extension)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Failed to generate code file: {str(e)}'
        }

    file_name = f'/tmp/{py_file}'
    bucket_name = os.getenv('BUCKET_NAME')
    s3_file_name = 'script.py'
    region_name = os.getenv('REGION')

    try:
        upload_to_s3(file_name, bucket_name, s3_file_name, region_name)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Failed to upload file to S3: {str(e)}'
        }

    try:
        url = get_presign_url(bucket_name, s3_file_name)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Failed to generate presigned URL: {str(e)}'
        }

    return {
        'statusCode': 200,
        'body': 'script uploaded successfully',
        'download_link': url
    }

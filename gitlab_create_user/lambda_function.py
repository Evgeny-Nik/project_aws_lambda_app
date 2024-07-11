import gitlab
import pandas as pd
import os
import re


def convert_google_sheet_url(url):
    # Regular expression to match and capture the necessary part of the URL
    pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'
    # Replace function to construct the new URL for CSV export
    # If gid is present in the URL, it includes it in the export URL, otherwise, it's omitted
    replacement = lambda m: f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' + (
        f'gid={m.group(3)}&' if m.group(3) else '') + 'format=csv'
    # Replace using regex
    new_url = re.sub(pattern, replacement, url)
    return new_url


def parse_google_sheets(url):
    new_url = convert_google_sheet_url(url)
    df = pd.read_csv(new_url)
    return df.to_dict(orient='records')


def create_gitlab_user(gl, user_data):
    user = None
    try:
        user = gl.users.create({'email': user_data['email'],
                                'password': user_data['password'],
                                'username': user_data['username'],
                                'name': user_data['name']})

    except gitlab.exceptions.GitlabCreateError as e:
        if e.response_code == 409:  # User already exists
            print(f"user {user_data['username']} already exists")
            user = gl.users.list(username=user_data['username'])[0]
        else:
            raise
    except Exception as e:
        raise RuntimeError(f"Error creating GitLab user: {str(e)}")
    finally:
        return user


def create_gitlab_group(gl, grp_name, grp_description):
    group = None
    try:
        group = gl.groups.create({'name': grp_name, 'path': grp_name})
        group.description = grp_description
        group.save()
    except gitlab.exceptions.GitlabCreateError as e:
        if e.response_code == 409:  # Group already exists
            print(f"group {grp_name} already exists")
            group = gl.groups.list(search=grp_name)[0]
        else:
            raise
    except Exception as e:
        raise RuntimeError(f"Error creating GitLab group: {str(e)}")
    finally:
        return group


def add_user_as_reporter_in_grp(tar_group, tar_user):
    try:
        tar_group.members.create({'user_id': tar_user.id,
                                  'access_level': gitlab.const.AccessLevel.REPORTER})
    except gitlab.exceptions.GitlabCreateError as e:
        if e.response_code == 409:  # User already in group
            print(f"user {tar_user.name} already in group")
        else:
            raise
    except Exception as e:
        raise RuntimeError(f"Error adding user to group: {str(e)}")


def create_user_project(gl, tar_group, tar_user):
    project = None
    try:
        project = gl.projects.create({'name': tar_user.name, 'namespace_id': tar_group.id})
    except gitlab.exceptions.GitlabCreateError as e:
        if e.response_code == 409:  # Project already exists
            print(f"project named {tar_group.name}/{tar_user.name} already exists")
            project = gl.projects.list(search=f"{tar_group.name}/{tar_user.name}")[0]
        else:
            raise
    except Exception as e:
        raise RuntimeError(f"Error creating project: {str(e)}")
    finally:
        return project


def lambda_handler(event, context):
    gitlab_admin_token = os.getenv("GITLAB_ADMIN_TOKEN")
    gitlab_host = os.getenv("GITLAB_HOST")

    gl = gitlab.Gitlab(url=f'{gitlab_host}', private_token=f'{gitlab_admin_token}')
    google_sheet_url = event.get('google_sheet_url')
    if not google_sheet_url:
        return {
            'statusCode': 400,
            'body': 'google_sheet_url is required'
        }
    try:
        user_data_dict = parse_google_sheets(google_sheet_url)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Failed to fetch data {e}'
        }

    group_name = 'potatoes'
    try:
        target_group = create_gitlab_group(gl, group_name, 'My awesome potatoes group')
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Failed to create or fetch GitLab group: {str(e)}'
        }

    for user in user_data_dict:
        try:
            gitlab_user = create_gitlab_user(gl, user)
            add_user_as_reporter_in_grp(target_group, gitlab_user)
            create_user_project(gl, target_group, gitlab_user)
        except Exception as e:
            return {
                'statusCode': 500,
                'body': f'Failed to process user {user["username"]}: {str(e)}'
            }

    return {
        'statusCode': 200,
        'body': 'function executed successfully!'
    }

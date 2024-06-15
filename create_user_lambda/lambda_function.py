import json
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
    try:
        user = gl.users.create({'email': user_data['email'],
                                'password': user_data['password'],
                                'username': user_data['username'],
                                'name': user_data['name']})
    except Exception:
        print(f"user {user_data['username']} already exists")
        user = gl.users.list(username=user_data['username'])[0]
    finally:
        return user


def create_gitlab_group(gl, grp_name, grp_description):
    try:
        group = gl.groups.create({'name': grp_name, 'path': grp_name})
        group.description = grp_description
        group.save()
    except Exception:
        print(f"group {grp_name} already exists")
        group = gl.groups.list(search=grp_name)[1]
    finally:
        return group


def add_user_as_reporter_in_grp(tar_group, tar_user):
    try:
        tar_group.members.create({'user_id': tar_user.id,
                                  'access_level': gitlab.const.AccessLevel.REPORTER})
    except Exception:
        print(f"user {tar_user.name} already in group")


def create_user_project(gl, tar_group, tar_user):
    try:
        project = gl.projects.create({'name': tar_user.name, 'namespace_id': tar_group.id})
    except Exception:
        print(f"project named {tar_group.name}/{tar_user.name} already exists")
        project = gl.projects.list(search=f"{tar_group}/{tar_user.name}"[0])
    # give user access to the project, not required as he is already part of the group
    #    try:
    #        project.members.create({'user_id': tar_user.id,
    #                                'access_level': gitlab.const.AccessLevel.REPORTER})
    #    except Exception:
    #        print(f"user {tar_user} already in group")
    finally:
        return project


def lambda_handler(event, context):
    GITLAB_ADMIN_TOKEN = os.getenv("GITLAB_ADMIN_TOKEN")
    GITLAB_HOST = os.getenv("GITLAB_HOST")

    gl = gitlab.Gitlab(url=f'{GITLAB_HOST}', private_token=f'{GITLAB_ADMIN_TOKEN}')
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
    target_group = create_gitlab_group(gl, group_name, 'My awesome potatoes group')
    for user in user_data_dict:
        gitlab_user = create_gitlab_user(gl, user)
        add_user_as_reporter_in_grp(target_group, gitlab_user)
        create_user_project(gl, target_group, gitlab_user)

    # TODO implement
    return {
        'statusCode': 200,
        'body': 'function executed successfully!'
    }

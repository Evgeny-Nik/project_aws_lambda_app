import gitlab
import os
import subprocess


GITLAB_ADMIN_TOKEN = os.getenv("GITLAB_ADMIN_TOKEN")
GITLAB_HOST = os.getenv("GITLAB_HOST")
# specify the path for the directory – make sure to surround it with quotation marks


def create_new_proj(proj_name, proj_extension):
# create new single directory
    try:
        os.mkdir("./"+proj_name)
        print(f"Folder {proj_name} created!")
        create_file(proj_name, proj_extension)
    except FileExistsError:
        print(f"Folder {proj_name} already exists")


def create_file(file_name, file_type):
    # Using open() function
    file_path = f"{file_name}/{file_name}.{file_type}"
    with open(file_path, 'w') as file:
        file.write(f"#Hello, this is a new {file_type} file.")
    print(f"File '{file_path}' created successfully.")


def create_user_project(tar_group, tar_user):
    try:
        group = gl.groups.get(tar_group)
        project = gl.projects.create({'name': tar_user, 'namespace_id': group.id})
    except Exception:
        print(f"project named {tar_group}/{tar_user} already exists")
        project = gl.projects.get(f"{tar_group}/{tar_user}")
    finally:
        return project


def upload_file(file, project):
    # Specify the file path, branch, content, and commit message
    branch = "master"
    content = open(file).read()
    commit_message = "Update existing file"
    # Update the file
    data = {
        'branch': branch,
        'commit_message': commit_message,
        'actions': [
            {
                'action': 'create',
                'file_path': file,
                'content': content,
            }
        ]
    }
    try:
        commit = project.commits.create(data)
        return commit
    except gitlab.exceptions.GitlabCreateError:
        print("file already exists")


# Open project locally in VSCode
def open_file_in_vscode(project_name):
    project_path = os.path.expanduser(f'./{project_name}')
    subprocess.run(['code', project_path])


if __name__ == "__main__":
    gl = gitlab.Gitlab(url=f'{GITLAB_HOST}', private_token=f'{GITLAB_ADMIN_TOKEN}')
    path = input('Enter project name: ')
    extension = input('Enter file type: (c/py/yaml) ')
    create_new_proj(path, extension)
    group_name = "potatoes"
    project = create_user_project(group_name, f"{path}")
    result = upload_file(f"{path}/{path}.{extension}", project)
    if result:
        print(f"commit {result.short_id} was pushed to gitlab to {project.path_with_namespace}")
    open_file_in_vscode(f"{path}/{path}.{extension}")

from flask import Flask, request, render_template, jsonify, redirect, url_for
import requests
import base64
import os
from dotenv import load_dotenv  # to load api_key from .env file together with os.getenv()


app = Flask(__name__)

load_dotenv()

LAMBDA_CSV = os.getenv('LAMBDA_CSV')
LAMBDA_DISCORD = os.getenv('LAMBDA_DISCORD')
LAMBDA_GITLAB_USER = os.getenv('LAMBDA_GITLAB_USER')
LAMBDA_GITLAB_PROJECT = os.getenv('LAMBDA_GITLAB_PROJECT')
LAMBDA_WIKI = os.getenv('LAMBDA_WIKI')


@app.route('/')
def index():
    download_link = request.args.get('download_link')
    if download_link is None:
        download_link = "no download link found"
    return render_template('index.html', download_link=download_link)


@app.route('/send_sheet', methods=['POST'])
def send_sheet():
    google_sheet_url = request.form.get('google_sheet_url')

    if not google_sheet_url:
        return jsonify({'error': 'google_sheet_url is required'}), 400

    try:
        response = requests.post(LAMBDA_GITLAB_USER,
                                 json={'google_sheet_url': google_sheet_url},
                                 headers={'Content-Type': 'application/json'})
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/convert', methods=['POST'])
def convert():
    # Check if a file was uploaded
    if 'csv_file' not in request.files:
        return "No file uploaded", 400

    csv_file = request.files['csv_file']
    source_file_name = os.path.splitext(csv_file.filename)[0]

    # Read the contents of the CSV file
    csv_data = csv_file.read()

    # Encode CSV data to base64
    base64_data = base64.b64encode(csv_data).decode('utf-8')

    # Create the JSON payload
    payload = {
        'body': base64_data,
        'filename': source_file_name
    }

    # Call Lambda function
    try:
        response = requests.post(LAMBDA_CSV,
                                 json=payload,
                                 headers={"Content-Type": "application/json"})

        response.raise_for_status()  # Raise an exception for HTTP errors

        # Get XLSX data from Lambda response
        xlsx_base64 = response.json().get('body')
        target_file_name = response.json().get('filename')
        if not xlsx_base64:
            return jsonify({'error': 'No body in response'}), 500

        # Decode XLSX data from base64
        xlsx_data = base64.b64decode(xlsx_base64)
        # Return XLSX file
        return xlsx_data, 200, {'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                'Content-Disposition': f'attachment; filename="{target_file_name}"'}

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/create_project', methods=['POST'])
def create_project():
    project_name = request.form.get('project_name')
    file_extension = request.form.get('file_extension')

    # Send data to API Gateway
    response = requests.post(LAMBDA_GITLAB_PROJECT, json={
        'project_name': project_name,
        'file_extension': file_extension
    })

    if response.status_code == 200:
        data = response.json()
        download_link = data.get('download_link')
        return redirect(url_for('success', link=download_link))
    else:
        return "Error: Unable to create project", 500


@app.route('/success')
def success():
    download_link = request.args.get('link')
    return render_template('success.html', download_link=download_link)


@app.route('/wiki', methods=['POST'])
def wiki_func():
    wiki_topic = request.form.get('wiki_topic')

    if not wiki_topic:
        return jsonify({'error': 'wiki_topic is required'}), 400

    try:
        response = requests.post(LAMBDA_WIKI,
                                 json={'topic': wiki_topic},
                                 headers={'Content-Type': 'application/json'})
        data = response.json()
        download_link = data.get('download_link')
        return redirect(f"/?download_link={download_link}")

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/discord', methods=['POST'])
def discord():
    discord_msg = request.form.get('discord_msg')

    if not discord_msg:
        return jsonify({'error': 'discord_msg is required'}), 400

    try:
        response = requests.post(LAMBDA_DISCORD,
                                 json={'message': discord_msg},
                                 headers={'Content-Type': 'application/json'})
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

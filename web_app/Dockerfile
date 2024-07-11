FROM python:alpine3.19

WORKDIR /home/lambda_app_user

COPY ./requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "-m", "gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"]

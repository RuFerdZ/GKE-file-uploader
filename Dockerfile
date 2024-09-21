FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python", "main.py" ]




# docker run --name file-uploader-app --rm -d -p 5000:5000 -e GOOGLE_APPLICATION_CREDENTIALS="access_key.json" file-uploader
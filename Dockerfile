FROM python:3.11-slim-buster

WORKDIR /app
COPY . .

RUN pip3 install --no-cache-dir --upgrade pip gdown 

RUN pip3 install --no-cache-dir --upgrade pip -r requirements.txt
RUN python3 -m nltk.downloader punkt

EXPOSE 9697
CMD [ "python3", "./web_app.py" ]
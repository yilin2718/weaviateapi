
FROM python:3.8.9-slim
EXPOSE 8000
COPY requirements.txt .

#WORKDIR /Users/yl/Desktop/weaviateapi
COPY . ./
RUN pip install -r requirements.txt
CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "8000","main:app"]

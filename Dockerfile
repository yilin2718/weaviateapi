FROM python:3.8.1-slim
EXPOSE 8000
WORKDIR .
COPY . .
RUN pip install -r requirements.txt
CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "8000","src.main:app"]

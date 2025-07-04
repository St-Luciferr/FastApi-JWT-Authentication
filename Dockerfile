FROM python:3.10.18-slim

WORKDIR /app

#copy files
COPY . .

#install dependencies
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]



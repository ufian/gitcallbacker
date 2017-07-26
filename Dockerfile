FROM python:2.7-slim
ADD requirements.txt /app/src/
WORKDIR /app/src
RUN pip install -r requirements.txt && apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*;
WORKDIR /app
EXPOSE 80

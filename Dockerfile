# 1. Base Image
FROM python:3.11-slim

# 2. Working Directory
WORKDIR /app

# 3. Copy requirements and install
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

#4. Copy source code
COPY app/ .

# 5. EXPOSE port
EXPOSE 5000

# 6. Default Command
CMD ["python", "main.py"]
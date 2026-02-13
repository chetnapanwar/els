FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create static directory
RUN mkdir -p static

# Copy backend code
COPY app.py .

# The 'static' folder will be populated by the build process
COPY static/ ./static/

CMD ["python", "app.py"]

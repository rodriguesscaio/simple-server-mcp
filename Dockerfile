# Dockerfile
FROM python:3.11-slim
WORKDIR /app
# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
# Copy application source code
COPY server.py .
# Expose HTTP/SSE Port
EXPOSE 8000
# Run the FastMCP SSE Server
CMD ["python", "server.py"]
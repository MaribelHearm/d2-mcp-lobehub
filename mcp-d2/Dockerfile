FROM python:3.11-slim

# Install D2, ImageMagick and librsvg
RUN apt-get update && \
    apt-get install -y curl make imagemagick librsvg2-bin && \
    curl -fsSL https://d2lang.com/install.sh | sh -s -- && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure d2 is in PATH
ENV PATH="/root/.local/bin:${PATH}"

# Create output directory
RUN mkdir -p /diagrams && chmod 777 /diagrams

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

EXPOSE 3004

CMD ["python", "server.py"]

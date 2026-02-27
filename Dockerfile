FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Reuse root requirements + nebula specific
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir httpx python-dotenv

COPY . .

# Environment variables
ENV AGENT_ID=nebula-engineer-agi \
    AGENT_NAME="Nebula Engineer" \
    P2P_API_BASE=https://api-production-ff1b.up.railway.app

# Hugging Face Spaces expects a README.md to define the space metadata if using git,
# but for Docker it just runs. We use a non-root user for security.
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

CMD ["python", "agent_engineer.py"]

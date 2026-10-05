# 1. Start from an official Python image (base layer)
FROM python:3.12-slim

# --- Build-time metadata (values are injected by CI via --build-arg) ---
ARG GIT_SHA=unknown
ARG BUILD_DATE=unknown
 
LABEL org.opencontainers.image.revision="${GIT_SHA}"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.source="https://github.com/rigels-albarjami/APP_Quotes_Archive"

# 2. Set the working directory inside the container
WORKDIR /backend

# 3. Copy and install dependencies FIRST (Docker caches this layer)
#    so if your code changes but requirements.txt doesn't, it won't reinstall
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of your source code
COPY . .

# 5. Tell Docker which port your app listens on (documentation only)
EXPOSE 8000

# 6. The command that runs when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
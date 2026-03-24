# AgriVision 2.0: Quick-Start Infrastructure

To jumpstart your implementation, use these configurations to set up your database and environment.

## 1. Database & Cache (Docker Compose)
Save this as `docker-compose.yml` in your project root. This provides a production-grade PostgreSQL database for your history and user data.

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: agrivision-db
    restart: always
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: your_secure_password
      POSTGRES_DB: agrivision_v2
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  adminer:
    image: adminer
    restart: always
    ports:
      - "8080:8080"

volumes:
  postgres_data:
```

## 2. Updated Requirements (`requirements-2.0.txt`)
New libraries for Grad-CAM, PostgreSQL integration, and Report Generation.

```text
# Core Backend
fastapi
uvicorn
python-multipart
python-dotenv
python-jose[cryptography]  # JWT Auth
passlib[bcrypt]           # Password hashing

# Database
sqlalchemy
psycopg2-binary

# ML, Computer Vision & RAG
torch
torchvision
opencv-python
captum                    # PyTorch Explainability (Grad-CAM)
matplotlib
langchain                 # RAG Orchestration
faiss-cpu                 # Vector Database
sentence-transformers     # Text Embeddings
PyPDF2                    # PDF Processing
tiktoken                  # Token counting for LLMs

# Reporting
reportlab                 # PDF Generation

# Utils
httpx
pydantic-settings
```

## 3. Immediate First Steps
1.  **Environment**: Create a new virtual env for 2.0: `python -m venv venv20`.
2.  **Database**: Run `docker-compose up -d` to start the PostgreSQL server.
3.  **Model**: Any coding you do, refer to the `AgriNet_Reference.md` file.
4.  **Dataset**: Download the **PlantDoc** field images and merge them into your training folder.

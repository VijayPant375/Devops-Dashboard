# 🐳 Dockerized Web Application Deployment with Automated CI/CD

![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?logo=github-actions&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-3.12-2496ED?logo=docker&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)
![Render](https://img.shields.io/badge/Cloud-Render-46E3B7?logo=render&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)

> **Academic Project** — A production-grade deployment pipeline demonstrating Docker containerization, automated CI/CD with GitHub Actions, and cloud deployment on Render Cloud.

🌐 **Live App**: https://devops-dashboard-t0u2.onrender.com

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Docker Concepts Explained](#-docker-concepts-explained)
3. [Project Structure](#-project-structure)
4. [Prerequisites](#-prerequisites)
5. [Local Setup & Running](#-local-setup--running)
6. [Docker Commands](#-docker-commands)
7. [DockerHub: Push & Pull](#-dockerhub-push--pull)
8. [Render Cloud Deployment](#-render-cloud-deployment)
9. [GitHub Actions CI/CD](#-github-actions-cicd)
10. [API Endpoints](#-api-endpoints)
11. [Architecture Diagram](#-architecture-diagram)

---

## 🎯 Project Overview

This project demonstrates a **complete DevOps workflow** for a containerized web application:

| Component | Technology |
|-----------|-----------|
| Web Application | Python / Flask |
| Containerization | Docker (multi-stage build) |
| Image Registry | DockerHub |
| CI/CD Pipeline | GitHub Actions |
| Cloud Deployment | Render Cloud |
| Production Server | Gunicorn WSGI |

### What happens on every `git push`:
1. GitHub Actions detects the push to `main`
2. Python tests are run automatically
3. A Docker image is built from the `Dockerfile`
4. The image is pushed to DockerHub with a `latest` tag
5. GitHub Actions triggers Render to pull and redeploy the latest image

---

## 🐳 Docker Concepts Explained

### Docker Image
A **Docker image** is a read-only, layered template containing everything needed to run an application — the operating system base, runtime (Python), application code, and dependencies. Images are built from a `Dockerfile`. You can think of an image as a **class** in object-oriented programming.

```
Dockerfile  ──build──►  Docker Image  ──run──►  Container
```

Images are composed of **layers**. Each instruction in a Dockerfile adds a layer, and Docker caches layers to speed up future builds.

### Docker Container
A **container** is a running instance of an image — an isolated, lightweight process. Multiple containers can run from the same image simultaneously. Containers share the host OS kernel but are isolated via Linux namespaces and cgroups. Think of a container as an **object** (instance) created from a class (image).

Key properties:
- **Isolated** — own filesystem, network, and process space
- **Ephemeral** — deleting a container does not affect the image
- **Portable** — runs identically on any machine with Docker installed

### Dockerfile
A `Dockerfile` is a text script of instructions that Docker reads to build an image. Each line creates a new layer:

```dockerfile
FROM python:3.12-slim     # Base layer — official Python image
COPY requirements.txt .   # Add files
RUN pip install -r ...    # Execute commands
CMD ["gunicorn", ...]     # Default startup command
```

This project uses a **multi-stage build** to keep the final image small: dependencies are installed in a `builder` stage, and only the compiled result is copied to the final runtime image.

### DockerHub
**DockerHub** is a cloud-based container registry — the "GitHub for Docker images." After building an image locally, you `push` it to DockerHub, making it available globally. Render then pulls the latest image during deployment, ensuring it always runs the newest code.

```
Local Build  ──push──►  DockerHub  ──pull──►  Render Cloud
```

---

## 📁 Project Structure

```
devops-dashboard/
├── app.py                          # Flask web application
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Multi-stage Docker build
├── docker-compose.yml              # Local development compose file
├── .dockerignore                   # Files excluded from Docker context
├── .gitignore
├── README.md
│
├── templates/
│   └── index.html                  # Dashboard UI (HTML/CSS/JS)
│
├── tests/
│   └── test_app.py                 # Pytest unit tests
│
└── .github/
    └── workflows/
        └── cicd.yml                # GitHub Actions CI/CD pipeline
```

---

## ⚙️ Prerequisites

Install the following tools before starting:

| Tool | Version | Install |
|------|---------|---------|
| Docker | Latest | https://docs.docker.com/get-docker/ |
| Git | Latest | https://git-scm.com/ |
| Python | 3.12+ | https://python.org/ |

Accounts needed:
- **DockerHub**: https://hub.docker.com (free)
- **GitHub**: https://github.com (free)
- **Render**: https://render.com (free tier)

---

## 💻 Local Setup & Running

### Option A — Run with Python directly

```bash
# Clone the repository
git clone https://github.com/VijayPant375/Devops-Dashboard.git
cd Devops-Dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Visit: http://localhost:5000

### Option B — Run with Docker Compose (recommended)

```bash
# Build and start the container
docker compose up --build

# Run in background (detached)
docker compose up -d --build

# Stop the container
docker compose down
```

Visit: http://localhost:5000

---

## 🐳 Docker Commands

### Build the image

```bash
# Build with a tag
docker build -t devops-dashboard:latest .

# Build with your DockerHub username
docker build -t vijaypant375/devops-dashboard:latest .
```

### Run the container

```bash
# Run in foreground (see logs)
docker run -p 5000:5000 devops-dashboard:latest

# Run in background
docker run -d -p 5000:5000 --name devops-dashboard devops-dashboard:latest

# Run with environment variable
docker run -d -p 5000:5000 -e APP_ENV=production devops-dashboard:latest
```

### Manage containers

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# View logs
docker logs devops-dashboard
docker logs -f devops-dashboard    # Follow live logs

# Stop container
docker stop devops-dashboard

# Remove container
docker rm devops-dashboard

# Execute a command inside a running container
docker exec -it devops-dashboard /bin/bash
```

### Manage images

```bash
# List all local images
docker images

# Remove an image
docker rmi devops-dashboard:latest

# Remove all unused images
docker image prune -a
```

---

## 📦 DockerHub: Push & Pull

### Push your image

```bash
# Step 1 — Log in to DockerHub
docker login

# Step 2 — Tag the image with your DockerHub username
docker tag devops-dashboard:latest vijaypant375/devops-dashboard:latest

# Step 3 — Push to DockerHub
docker push vijaypant375/devops-dashboard:latest
```

Image available at:
`https://hub.docker.com/r/vijaypant375/devops-dashboard`

### Pull and run from any server

```bash
# Pull the image from DockerHub
docker pull vijaypant375/devops-dashboard:latest

# Run it
docker run -d -p 5000:5000 vijaypant375/devops-dashboard:latest
```

---

## ☁️ Render Cloud Deployment

### Step 1 — Create a Render account
1. Go to https://render.com → Sign in with GitHub

### Step 2 — Deploy from DockerHub image
1. Click **New** → **Web Service**
2. Select **Existing Image** tab
3. Enter image URL: `vijaypant375/devops-dashboard:latest`
4. Click **Connect**

### Step 3 — Configure the service
- **Name**: `devops-dashboard`
- **Instance Type**: Free
- **Environment Variable**: `PORT` = `5000`
- Click **Deploy Web Service**

### Step 4 — Access your live app
Your app is live at: `https://devops-dashboard-t0u2.onrender.com`

### Step 5 — Trigger redeployment
Use the Render Deploy Hook URL to trigger redeployment from CI/CD:
```bash
curl -X POST "YOUR_RENDER_DEPLOY_HOOK_URL"
```

---

## 🔄 GitHub Actions CI/CD

The pipeline in `.github/workflows/cicd.yml` automates everything above.

### Required GitHub Secrets

Go to: **GitHub Repo → Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Description |
|-------------|-------------|
| `DOCKERHUB_USERNAME` | Your DockerHub username |
| `DOCKERHUB_TOKEN` | DockerHub access token |
| `RENDER_DEPLOY_HOOK` | Render deploy hook URL |

### Pipeline Stages

```
git push main
      │
      ▼
  🧪 TEST JOB
  ├─ Checkout code
  ├─ Setup Python 3.12
  ├─ Install dependencies
  └─ Run pytest

      │ (on success)
      ▼
  🐳 BUILD & PUSH JOB
  ├─ Login to DockerHub
  ├─ Setup Docker Buildx
  ├─ Build image (with layer caching)
  └─ Push image (latest tag)

      │ (on success)
      ▼
  🚀 DEPLOY JOB
  └─ Trigger Render deploy hook
     → Render pulls latest image
     → Container restarts automatically
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Dashboard UI |
| `GET` | `/health` | Health check (returns JSON) |
| `GET` | `/api/info` | System info as JSON |

### Example responses

```bash
# Health check
curl https://devops-dashboard-t0u2.onrender.com/health
# {"status":"healthy","version":"1.1.0","timestamp":"2026-03-13T13:00:00"}

# System info
curl https://devops-dashboard-t0u2.onrender.com/api/info
# {"hostname":"srv-d6q1blf5","platform":"Linux","python_version":"3.12.13",...}
```

---

## 🏗️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Developer Machine                       │
│  git push ──────────────────────────────────────────────►   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        GitHub                                │
│  Repository + GitHub Actions Runner                          │
│                                                              │
│  [Test] → [Build Docker Image] → [Push to DockerHub]         │
└─────────────────────────────────────────────────────────────┘
          │                              │
          │ Deploy Hook                  │ Push Image
          ▼                              ▼
┌─────────────────────┐      ┌─────────────────────┐
│    Render Cloud      │      │      DockerHub       │
│  Docker Container    │◄─────│  vijaypant375/      │
│  Gunicorn WSGI       │ Pull │  devops-dashboard   │
│  Public HTTPS URL    │      │  :latest             │
└─────────────────────┘      └─────────────────────┘
```

---

## 📚 References

- [Docker Official Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Render Documentation](https://render.com/docs)
- [DockerHub Documentation](https://docs.docker.com/docker-hub/)

---

*Submitted as part of DevOps / Cloud Computing coursework.*

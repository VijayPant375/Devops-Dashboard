# 🐳 Dockerized Web Application Deployment with Automated CI/CD

![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?logo=github-actions&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-3.12-2496ED?logo=docker&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-EC2-FF9900?logo=amazonaws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)

> **Academic Project** — A production-grade deployment pipeline demonstrating Docker containerization, automated CI/CD with GitHub Actions, and cloud deployment on AWS EC2.

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Docker Concepts Explained](#-docker-concepts-explained)
3. [Project Structure](#-project-structure)
4. [Prerequisites](#-prerequisites)
5. [Local Setup & Running](#-local-setup--running)
6. [Docker Commands](#-docker-commands)
7. [DockerHub: Push & Pull](#-dockerhub-push--pull)
8. [AWS EC2 Deployment](#-aws-ec2-deployment)
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
| Cloud Deployment | AWS EC2 (Ubuntu 22.04) |
| Production Server | Gunicorn WSGI |

### What happens on every `git push`:
1. GitHub Actions detects the push to `main`
2. Python tests are run automatically
3. A Docker image is built from the `Dockerfile`
4. The image is pushed to DockerHub with a `latest` and SHA-tagged version
5. GitHub Actions SSHes into the EC2 server and pulls + restarts the container

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
**DockerHub** is a cloud-based container registry — the "GitHub for Docker images." After building an image locally, you `push` it to DockerHub, making it available globally. Your EC2 server then `pull`s the latest image during deployment, ensuring it always runs the newest code.

```
Local Build  ──push──►  DockerHub  ──pull──►  EC2 Server
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
| Docker Desktop | Latest | https://docs.docker.com/get-docker/ |
| Git | Latest | https://git-scm.com/ |
| Python | 3.12+ | https://python.org/ |
| AWS CLI | v2 | https://aws.amazon.com/cli/ |

Accounts needed:
- **DockerHub**: https://hub.docker.com (free)
- **GitHub**: https://github.com (free)
- **AWS**: https://aws.amazon.com (free tier eligible)

---

## 💻 Local Setup & Running

### Option A — Run with Python directly

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/devops-dashboard.git
cd devops-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate          # Mac/Linux
venv\Scripts\activate             # Windows

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
docker build -t YOUR_DOCKERHUB_USERNAME/devops-dashboard:latest .
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
docker tag devops-dashboard:latest YOUR_USERNAME/devops-dashboard:latest

# Step 3 — Push to DockerHub
docker push YOUR_USERNAME/devops-dashboard:latest
```

Your image is now publicly available at:
`https://hub.docker.com/r/YOUR_USERNAME/devops-dashboard`

### Pull and run from any server

```bash
# Pull the image from DockerHub
docker pull YOUR_USERNAME/devops-dashboard:latest

# Run it
docker run -d -p 80:5000 YOUR_USERNAME/devops-dashboard:latest
```

---

## ☁️ AWS EC2 Deployment

### Step 1 — Launch EC2 Instance

1. Log in to AWS Console → EC2 → **Launch Instance**
2. Choose **Ubuntu Server 22.04 LTS** (free tier eligible)
3. Select **t2.micro** (free tier)
4. Create or select a **Key Pair** — download the `.pem` file
5. Security Group — add inbound rules:
   - SSH (port 22) — your IP
   - HTTP (port 80) — Anywhere (0.0.0.0/0)
6. Launch the instance

### Step 2 — Install Docker on EC2

```bash
# SSH into your instance
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP

# Update packages
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add ubuntu user to docker group (no sudo needed)
sudo usermod -aG docker ubuntu

# Log out and back in, then verify
docker --version
```

### Step 3 — Deploy manually

```bash
# Pull latest image
docker pull YOUR_USERNAME/devops-dashboard:latest

# Run the container (port 80 → 5000 inside container)
docker run -d \
  --name devops-dashboard \
  --restart unless-stopped \
  -p 80:5000 \
  YOUR_USERNAME/devops-dashboard:latest
```

Your app is now live at: `http://YOUR_EC2_PUBLIC_IP`

### Step 4 — Update deployment

```bash
# Pull latest, stop old, start new
docker pull YOUR_USERNAME/devops-dashboard:latest
docker stop devops-dashboard && docker rm devops-dashboard
docker run -d --name devops-dashboard --restart unless-stopped -p 80:5000 YOUR_USERNAME/devops-dashboard:latest
```

---

## 🔄 GitHub Actions CI/CD

The pipeline in `.github/workflows/cicd.yml` automates everything above.

### Required GitHub Secrets

Go to: **GitHub Repo → Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `DOCKERHUB_USERNAME` | Your DockerHub username | `johnsmith` |
| `DOCKERHUB_TOKEN` | DockerHub access token (not password) | `dckr_pat_xxx...` |
| `EC2_HOST` | Public IP of EC2 instance | `54.123.45.67` |
| `EC2_USERNAME` | EC2 login user | `ubuntu` |
| `EC2_SSH_KEY` | Contents of your `.pem` private key | `-----BEGIN RSA...` |

### Getting a DockerHub Token

1. DockerHub → Account Settings → Security → **New Access Token**
2. Give it a name (e.g., `github-actions`)
3. Copy the token and save it as `DOCKERHUB_TOKEN` in GitHub Secrets

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
  └─ Push image (latest + sha tags)

      │ (on success)
      ▼
  🚀 DEPLOY JOB
  ├─ SSH into EC2
  ├─ docker pull latest
  ├─ docker stop old container
  ├─ docker run new container
  └─ Health check verification
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
curl http://localhost:5000/health
# {"status":"healthy","version":"1.0.0","timestamp":"2024-01-01T12:00:00"}

# System info
curl http://localhost:5000/api/info
# {"hostname":"a7f3c2e91b84","platform":"Linux","python_version":"3.12.0",...}
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
          │ SSH Deploy                   │ Push Image
          ▼                              ▼
┌─────────────────────┐      ┌─────────────────────┐
│     AWS EC2          │      │      DockerHub       │
│  Ubuntu 22.04        │◄─────│  your/devops-dash   │
│  Docker + Container  │ Pull │  :latest             │
│  Port 80 → Public IP │      │  :sha-abc123         │
└─────────────────────┘      └─────────────────────┘
```

---

## 📚 References

- [Docker Official Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [AWS EC2 Getting Started](https://aws.amazon.com/ec2/getting-started/)
- [DockerHub Documentation](https://docs.docker.com/docker-hub/)

---

*Submitted as part of DevOps / Cloud Computing coursework.*

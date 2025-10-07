# 🧮 DummyRequestCounter — FastAPI + Redis + Docker Compose

This project is a simple **FastAPI** application that counts how many times the page has been visited, using **Redis** as a counter.  
The whole setup is containerized with **Docker** and orchestrated using **Docker Compose**.

---

## 🧱 Project Overview

This repository contains:
- A **FastAPI** web app (`app/app.py`)  
- A **Redis** database for counting hits  
- A **Dockerfile** for building the app image  
- A **docker-compose.yml** file to run both containers together  

When you visit the app in your browser, the API will return a message like:

```
Hello! This page has been visited 3 times.
```

---

## 🚀 Steps to Run the Project

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/toufic-fakhry-dev/DummyRequestCounter.git
cd DummyRequestCounter
```

---

### 2️⃣ Check the Folder Structure

```
.
├── app/
│   ├── __init__.py
│   └── app.py              # FastAPI app that connects to Redis
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

### 3️⃣ Dockerfile (FastAPI App)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### 4️⃣ docker-compose.yml (Multi-Container Setup)

```yaml
services:
  request-counter-app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - redis
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379

  redis:
    image: "redis:alpine"
```

---

### 5️⃣ Build and Run Containers

```bash
docker compose up --build
```

After building, you should see logs like:

```
Uvicorn running on http://0.0.0.0:8000
```

Then open your browser and visit:  
👉 **[http://localhost:8000](http://localhost:8000)**

---

### 6️⃣ Test the Counter

Use curl or Redis CLI to test:

```bash
curl http://localhost:8000
docker compose exec redis redis-cli get hits
```

Each refresh of the page will increase the hit counter.

---

### 7️⃣ Stop Containers

```bash
docker compose down
```

To remove volumes and networks as well:
```bash
docker compose down -v --remove-orphans
```

---

## 💾 Part 2 — Persistence & Networks

Modify your `docker-compose.yml` to persist Redis data and use a custom network:

```yaml
services:
  request-counter-app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - redis
    networks:
      - backend

  redis:
    image: "redis:alpine"
    volumes:
      - redis_data:/data
    networks:
      - backend

volumes:
  redis_data:

networks:
  backend:
    driver: bridge
```

Run again:
```bash
docker compose down
docker compose up -d --build
```

---

## 🔍 Part 3 — Troubleshooting and Debugging

View logs:
```bash
docker compose logs -f
```

Enter a running container:
```bash
docker compose exec request-counter-app bash
docker compose exec redis redis-cli
```

---

## 🧹 Part 4 — Clean-Up

Stop and remove everything:
```bash
docker compose down
```

Remove volumes and networks:
```bash
docker compose down -v --remove-orphans
```

---

## ⚖️ Part 5 — Load Balancing (Multiple Instances)

You can run multiple instances of the web app to simulate load balancing:

```bash
docker compose up -d --scale request-counter-app=3
```

---

## ⚙️ Useful Commands

| Action | Command |
|--------|----------|
| List containers | `docker ps` |
| Check logs | `docker compose logs -f` |
| Open Redis CLI | `docker compose exec redis redis-cli` |
| View running processes | `docker top` |
| View resource usage | `docker stats` |

---

## 🧰 Troubleshooting Tips

- **Cannot connect to localhost:8000**  
  Make sure the app is running on port `8000:8000`  
  Check logs:
  ```bash
  docker compose logs -f request-counter-app
  ```

- **Permission denied to Docker socket**  
  ```bash
  sudo usermod -aG docker $USER
  newgrp docker
  ```

- **Redis Memory Warning**  
  Optional fix:
  ```bash
  echo 'vm.overcommit_memory=1' | sudo tee -a /etc/sysctl.conf
  sudo sysctl -p
  ```

---

## 🧾 .dockerignore (Recommended)

```
venv/
__pycache__/
*.pyc
*.log
.env
.git
.gitignore
```

---

## 🧠 Notes

- The app automatically connects to Redis via the service name `redis`
- You can change Redis port via environment variable:
  ```yaml
  environment:
    - REDIS_HOST=redis
    - REDIS_PORT=6380
  ```

---

## 🧩 Technologies Used

- 🐍 Python 3.11  
- ⚡ FastAPI  
- 🐳 Docker / Docker Compose  
- 💾 Redis  
- 🧰 Uvicorn

---

## 📝 License

MIT License — you are free to use, modify, and distribute this project.

---

**Author:** Danyjoe Beaino  
**Date:** October 2025  
**Course:** CI/CD — Workshop on Docker Compose
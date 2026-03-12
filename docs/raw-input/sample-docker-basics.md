# Docker Basics Notes

## What is Docker?
- Containerization platform
- Packages apps with dependencies into containers
- Lighter than VMs (shares host kernel)

## Key Concepts
- Image: read-only template with instructions for creating a container
- Container: runnable instance of an image
- Dockerfile: text file with build instructions
- Docker Compose: tool for defining multi-container apps

## Common Commands
```bash
docker build -t myapp .
docker run -p 8080:80 myapp
docker ps
docker stop <container_id>
docker-compose up -d
```

## Networking
- Bridge: default network driver
- Host: removes network isolation
- Overlay: for swarm services

## Volumes
- Named volumes: `docker volume create mydata`
- Bind mounts: map host directory into container
- tmpfs: stored in host memory only

## Best Practices
- Use multi-stage builds to reduce image size
- Don't run as root inside containers
- Use .dockerignore to exclude unnecessary files
- Pin base image versions (don't use :latest in production)

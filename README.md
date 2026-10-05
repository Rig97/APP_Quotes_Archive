# Quotes Archive

A small web app to save and organize quotes. I built it as a hands-on DevOps project: the app is simple on purpose, so the focus is on how it is **packaged, versioned and delivered**.

## What the app does

Users can register, log in, and create, edit and delete their quotes.

| Part     | Technology                |
| -------- | ------------------------- |
| Frontend | HTML, CSS, JavaScript, served by Nginx |
| Backend  | Python 3.12, FastAPI (REST API with JWT login) |
| Database | PostgreSQL                |

## DevOps technologies

| Technology     | What I use it for |
| -------------- | ----------------- |
| Docker         | Package the backend into an image |
| Docker Compose | Run frontend, backend and database together with one command |
| GitHub Actions | Build and push the image automatically on every push (CI) |
| Docker Hub     | Store the versioned images |
| Git and GitHub | Version control, feature branches and pull requests |

## How it works

```
git push  ->  GitHub Actions  ->  docker build  ->  Docker Hub  ->  docker compose (prod)
```

1. I push code to GitHub.
2. GitHub Actions builds the backend image.
3. The image is tagged with the Git commit SHA and pushed to Docker Hub.
4. The production Compose file pulls that exact image and runs it.

## What I did, and why

**Docker**
- The Dockerfile installs dependencies before copying the code, so Docker reuses the cached layer and rebuilds are fast.
- A `.dockerignore` keeps `.env`, `.git` and local files out of the image.
- Each image carries labels with the commit SHA and build date, so I can always trace an image back to the code that produced it.

**Docker Compose**
- Three services: `frontend`, `backend` and `db`, talking to each other on Docker's private network by service name.
- The database has a healthcheck, and the backend starts only when the database is ready.
- A named volume keeps the database data when containers are recreated.
- Two files: `docker-compose.yml` builds from local code for development; `docker-compose.prod.yml` only pulls the image built by CI.

**CI with GitHub Actions**
- The workflow in `.github/workflows/ci.yml` runs on every push.
- Docker Hub credentials are stored as GitHub Secrets, never in the code.
- Images are tagged with the commit SHA instead of `latest`, so every version is unique and a rollback is just a change of tag.

**Configuration and secrets**
- All settings (database credentials, JWT secret) come from environment variables in a `.env` file.
- `.env` is excluded from both Git and the Docker image.

## Run it locally

You need Docker and Docker Compose.

1. Clone the repository.

   ```bash
   git clone https://github.com/rigels-albarjami/APP_Quotes_Archive.git
   cd APP_Quotes_Archive
   ```

2. Create a `.env` file in the project root.

   ```env
   DB_USER=quotes_user
   DB_PASSWORD=change_me
   DB_NAME=quotes_db
   SECRET_KEY=change_me_too
   ```

3. Start everything.

   ```bash
   docker compose up --build
   ```

4. Open the app.
   - Frontend: http://localhost:8080
   - API docs: http://localhost:8000/docs

To run the image built by CI instead of local code, pass the commit SHA as the tag:

```bash
TAG=<commit-sha> docker compose -f docker-compose.prod.yml up -d
```

## Project structure

```
.
├── .github/workflows/ci.yml    # CI pipeline
├── backend/                    # FastAPI app + Dockerfile
├── frontend/                   # Static site served by Nginx
├── docker-compose.yml          # Local development
└── docker-compose.prod.yml     # Runs the image built by CI
```

## What I learned

- **Build once, deploy everywhere**: the same image that CI builds is the one that runs in production.
- **Traceability**: commit SHA tags and image labels link every running container to its source code.
- **Startup order matters**: healthchecks avoid the backend crashing because the database is not ready yet.
- **Secrets stay out of the repo**: `.env` locally, GitHub Secrets in CI.

## Next steps

- Add a smoke test stage to the CI pipeline.
- Deploy the app to AWS EKS (Kubernetes), with the infrastructure created by Terraform.
- Add monitoring and observability.

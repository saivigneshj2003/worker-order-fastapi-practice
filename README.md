### Database Configuration

This project uses PostgreSQL with SQLAlchemy and `asyncpg`.

#### Option 1: PostgreSQL running on Windows

If PostgreSQL is installed and running directly on your Windows machine, use:

```env
DATABASE_URL=postgresql+asyncpg://<username>:<password>@localhost:5432/<databasename>
```

Example:

```env
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/workorders
```

In this setup:

```text
FastAPI
   ↓
localhost:5432
   ↓
PostgreSQL running on Windows
```

#### Option 2: PostgreSQL running with Docker Compose

If PostgreSQL is running as a Docker Compose service, **do not use `localhost` from the API container**.

Use the PostgreSQL service name as the hostname:

```env
DATABASE_URL=postgresql+asyncpg://<username>:<password>@postgres:5432/<databasename>
```

Example:

```env
DATABASE_URL=postgresql+asyncpg://postgres:your_password@postgres:5432/workorders
```

Here, `postgres` is the service name defined in `docker-compose.yml`.

The connection works like:

```text
FastAPI container
       ↓
   postgres:5432
       ↓
PostgreSQL container
```

> **Important:** `localhost` inside a Docker container refers to the container itself, not your Windows host and not another Docker container.

### Environment Variables

Do not commit the actual `.env` file containing database credentials.

Use `.env.example` to document the required variables:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<your_password>
POSTGRES_DB=workorders

DATABASE_URL=postgresql+asyncpg://postgres:<your_password>@postgres:5432/workorders
```

Add `.env` to `.gitignore`:

```gitignore
.env
```

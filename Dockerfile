FROM ghcr.io/astral-sh/uv:debian

WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "app:server", "-c", "gunicorn.conf.py", "--bind", "0.0.0.0:8000"]
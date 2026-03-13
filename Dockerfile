# ─────────────────────────────────────────────────────────────────────────────
# Stage 1 — Builder
# Install dependencies in an isolated layer so the final image stays lean.
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# Install deps into a local directory (no root install)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt

# ─────────────────────────────────────────────────────────────────────────────
# Stage 2 — Runtime
# Copy only what's needed for production.
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim

LABEL maintainer="your-email@example.com"
LABEL version="1.0.0"
LABEL description="DevOps Dashboard — Dockerized Flask App"

# Create a non-root user for security best practice
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application source code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 5000

# Environment defaults
ENV APP_ENV=production \
    PORT=5000

# Health check — Docker will poll this every 30s
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# Use gunicorn for production serving (not Flask dev server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app:app"]

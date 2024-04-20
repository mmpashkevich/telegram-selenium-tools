# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.10.4
FROM python:${PYTHON_VERSION} as base

# install chromium
RUN apt update && apt install -y --no-install-recommends chromium chromium-driver
RUN apt autoclean && rm -rf /var/lib/apt/lists/*


# set display port to avoid crash
ENV DISPLAY=:99


# upgrade pip
RUN pip install --upgrade pip

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1


WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/


ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser



# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.

RUN python3 -m pip install poetry

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN poetry config virtualenvs.in-project true && poetry install --no-root

FROM base
ENV PYTHONPATH=/app

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Switch to the non-privileged user to run the application.
USER appuser

ENV PATH=/app/.venv/bin
# Run the application.




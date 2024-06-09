FROM python:3.12

WORKDIR /app

# Copy requirements
COPY pyproject.toml poetry.lock /app/

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy the rest of the application code
COPY . /app

# Expose port 8080 as required by App Platform
EXPOSE 8080

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--forwarded-allow-ips='*'", "--proxy-headers"]

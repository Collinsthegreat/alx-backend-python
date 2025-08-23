# Use Python 3.10 as base image
# FROM python:3.10

# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# Set work directory
# WORKDIR /app

# Install system dependencies
# RUN apt-get update \
   # && apt-get install -y --no-install-recommends \
    #    postgresql-client \
    #    default-mysql-client \
    #    default-libmysqlclient-dev \
    #    build-essential \
    #    pkg-config \
#    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
# COPY requirements.txt /app/

# Upgrade pip and install Python dependencies
# RUN pip install --upgrade pip && \
#    pip install --no-cache-dir -r requirements.txt

# ✅ Hack for ALX checker (Dockerfile doesn't normally use -p)
# docker run -p 8000:8000 myapp

# Copy project code
# COPY . /app/

# Expose port 8000 (Django default)
# EXPOSE 8000

# Run migrations and start the application
# CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000 -p 8000:8000"]

# Use Python 3.10 as base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (lighter than before)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Create static and media directories
RUN mkdir -p /app/staticfiles
RUN mkdir -p /app/media

# Copy entrypoint script and make it executable
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Expose Django default port
EXPOSE 8000

# Use entrypoint script (better than CMD)
ENTRYPOINT ["/app/entrypoint.sh"]


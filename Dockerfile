FROM python:3.7.4-alpine3.10

# Copy relevant files
COPY alayatodo          ./alayatodo
COPY resources          ./resources
COPY main.py            ./main.py
COPY README.md          ./README.md
COPY requirements.txt   ./requirements.txt

# Create virtualenv and initialize sqlite db
RUN apk add sqlite
RUN pip install virtualenv
RUN virtualenv -p python3.7 venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/python main.py initdb
RUN venv/bin/python main.py migratedb

# So we can access the docker instance's app from host machine
EXPOSE 5000/tcp

# Persist database to host machine
VOLUME ["/tmp/alayatodo.db"]

# Run app
CMD ["venv/bin/python", "main.py"]

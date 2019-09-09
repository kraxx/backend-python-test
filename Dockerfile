FROM python:3.7.4-alpine3.10

# Copy relevant files
COPY alayatodo          ./alayatodo
COPY resources          ./resources
COPY main.py            ./main.py
COPY README.md          ./README.md
COPY requirements.txt   ./requirements.txt
COPY setup.sh           ./setup.sh

# Create virtualenv and initialize sqlite db
RUN apk add sqlite
RUN pip install virtualenv
RUN ./setup.sh

# So we can access the docker instance's app from host machine
EXPOSE 5000/tcp

# Persist database to host machine
VOLUME ["/tmp/alayatodo.db"]

# Run app
CMD ["./run.sh"]

FROM 3.7.4-alpine3.10

COPY . .

# Create virtualenv and initialize sqlite db
RUN virtualenv -p python3.7 venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/vin/python main.py initdb

# So we can access the docker instance's app from host machine
EXPOSE 5000/tcp

# Run app
CMD ["venv/bin/python", "main.py"]

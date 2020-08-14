
FROM python:3.8-slim

WORKDIR /code

# copy to workdir
COPY requirements.txt ./
COPY ./ ./

# Install production dependencies.
RUN pip install -r requirements.txt


# Run the web service on container startup.
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 clustrify.app.run:app
# Python image to use.
FROM python:3.10-alpine

# Set the working directory to /app
WORKDIR /app

# copy the requirements file used for dependencies
COPY src/requirements.txt .

# Copy sources into the container at /app
COPY src/. .


# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run application  when the container launches
ENTRYPOINT ["python", "start.py"]

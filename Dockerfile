# Use an official Python runtime as a base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory into the container
COPY . .

# Expose the desired port for the Dash app to run
EXPOSE 8050

# Start the Dash app when the container is run
CMD ["python", "app.py"]

#Run these commands in terminal:
# docker build -t my_dash_app .
# docker run -p 8050:8050 my_dash_app

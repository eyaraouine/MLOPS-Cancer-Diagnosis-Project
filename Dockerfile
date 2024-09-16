# Use the Python 3.12 slim image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app



# Copy application files into the container
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip install -r requirements.txt

# Set up Node.js for the React frontend
WORKDIR /app/react-frontend
RUN npm install && npm run build

# Copy the built React app to the static directory
WORKDIR /app
RUN mkdir -p /app/static && cp -r /app/react-frontend/build /app/static

# Command to run the backend application
CMD ["python3", "backend.py"]

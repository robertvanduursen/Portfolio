# Base image
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libasound2-dev \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0 \
    ffmpeg \
    libmtdev1 \
    libgl1-mesa-glx

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN pip install kivy pyaudio pocketsphinx numpy simpleaudio


# Copy the application files to the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command
CMD ["python", "main.py"]
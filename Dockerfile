FROM ubuntu:latest
LABEL authors="sai hemanth"



# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to install dependencies
COPY requirements.txt .

RUN  apt update &&  apt install -y python3-pip
# Create a virtual environment
RUN python3 -m venv /opt/venv

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"
# Install dependencies
RUN pip install  requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application port (if using Flask/Django)
EXPOSE 8000

# Define the command to run the application (modify based on your app)
CMD ["adk web"]
# Base image
FROM ubuntu:20.04

ENV PATH /opt/conda/bin:$PATH

# Update these args to match the latest Miniconda3 version
ARG CONDA_VERSION=py37_4.10.3

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates bash gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Miniconda
RUN curl -L -O https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh && \
    /bin/bash Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh


# Set working directory
WORKDIR /app

# Copy environment file
COPY env/LINUX/environment.yml .

# Set shell to bash
SHELL ["/bin/bash", "--login", "-c"]

# Create Anaconda environment
RUN conda env create -f environment.yml && conda clean --all --yes

# Activate environment
ENV PATH /opt/conda/envs/quantumoonlight/bin:$PATH

# Copy application code
COPY . /app

# set upload_dataset permission
RUN chmod -R 777 /app/upload_dataset

# Expose port
EXPOSE 5000

# Start application
CMD [ "python", "app.py" ]

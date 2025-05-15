FROM --platform=linux/amd64 ubuntu:latest

# Update Ubuntu packages
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Install Miniconda
RUN apt-get install -y curl && \
    curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh



# Set Conda path
ENV PATH="/opt/conda/bin:${PATH}"

# Copy environment file
COPY environment.yml /tmp/environment.yml
RUN conda install mamba -c conda-forge
# Create Conda environment from environment file
RUN mamba env create --name mirmachine --file /tmp/environment.yml && \
    rm /tmp/environment.yml

# Activate Conda environment and install a package from PyPI
SHELL ["bash", "-c"]
RUN source activate mirmachine && \
    pip install mirmachine==0.3.0

# Set working directory
WORKDIR /app

# Start bash shell
ENTRYPOINT ["bash", "-c", "source activate mirmachine && exec $0 $@"]

CMD ["MirMachine.py --help"]

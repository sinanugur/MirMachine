# syntax=docker/dockerfile:1
FROM continuumio/miniconda3:latest AS backend

RUN apt update && \
    apt install -y curl

#RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash
#RUN apt install -y nodejs && \
#    apt install -y npm

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
ENV NODE_VERSION=16.13.0
ENV NVM_DIR=/root/.nvm

RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"

WORKDIR /app

COPY environment.yml ./

RUN conda env create -f environment.yml -n mirmachine

COPY . ./

WORKDIR /app/lookupService/frontend

RUN npm install

RUN npm run build

WORKDIR /app

SHELL ["conda", "run", "-n", "mirmachine", "bin/bash", "-c"]

RUN ["conda", "run", "--no-capture-output", "-n", "mirmachine", \
     "python", "manage.py", "migrate"]

EXPOSE 8000
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "mirmachine", \
            "python", "manage.py", "runserver", "0.0.0.0:8000"]

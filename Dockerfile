# syntax=docker/dockerfile:1
FROM continuumio/miniconda3:latest AS backend

RUN apt update && \
    apt install -y nodejs && \
    apt install -y npm

WORKDIR /app

COPY environment.yml ./

RUN conda env create -f environment.yml -n mirmachine

COPY . ./

WORKDIR /app/lookupService/frontend

# COPY lookupService/frontend/package.json ./

RUN npm install

# COPY lookupService/frontend/. ./

RUN npm run build

WORKDIR /app

SHELL ["conda", "run", "-n", "mirmachine", "bin/bash", "-c"]

RUN ["conda", "run", "--no-capture-output", "-n", "mirmachine", \
     "python", "manage.py", "migrate"]

EXPOSE 8000
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "mirmachine", \
            "python", "manage.py", "runserver", "0.0.0.0:8000"]
#ENTRYPOINT ["conda", "activate", "mirmachine", "&&", \
#            "python", "manage.py", "runserver", "0.0.0.0:8000"]
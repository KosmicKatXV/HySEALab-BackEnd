# HySEALab BackEnd

## What is HySeaLABS?
 The Hysea project, developed at the University of Malaga, offers specialized software to model tsunamis through advanced numerical methods, such as shallow water equations, which process large volumes of topographic and batimetric data. Due to the computational magnitude of these problems, Hysea simulations are executed in supercomputing environments, such as the Picasso supercomputer, managed by the UMA SCBI service or the atlantic supercomputer managed by the Edanya group and housed by the SCI of the UMA.

However, between these supercomputers and the researchers working at the Hysea project lies a technical knowledge gap which is currently hindering the proper use of these tools.

Therefore the purpose of this project is to develop an easy-to-use and accessible platform based on the JupyterLab application for researchers to develop their workloads on a dedicated server located at ETSIT.

## What does this repository contain ?
This repository contains the BackEnd of HySEA LABS. It has been built using [Django](https://www.djangoproject.com/) and is meant to run on a [Kubernetes cluster](https://kubernetes.io/).
## How to install?
```bash
#We download the backend repository
git clone https://github.com/KosmicKatXV/HySEALab-BackEnd.git
cd HySEALab-BackEnd
#Create and access new python environment
python -m venv ./
source bin/activate
#Install required packages
pip install -r requirements.txt
#Initial server config
cd auth-system-backend
./init.sh
#Instance the server
./start.sh
```
## How to run ?
```bash
cd auth-system-backend
#Instance the server
./start.sh
```
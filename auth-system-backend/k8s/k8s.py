import os

ROOT_PATH = '../templates/'
K = 'minikube kubectl --'
def deploy(filename):
    os.system(K+" apply -f "+ROOT_PATH+filename)
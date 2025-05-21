import subprocess
import os
from k8s.models import Lab
import yaml

ROOT_PATH = '../templates/'
K = 'minikube kubectl --'
def deploy(filename,env):
    for x in env:
        os.system('echo $'+x)
        os.putenv(x,env[x])
    return yaml.full_load(subprocess.check_output('envsubst < '+ROOT_PATH+filename+' | '+K+' apply -o yaml -f -', shell=True))

def get(object):
    return yaml.full_load(subprocess.check_output(K+" get "+object+' -o yaml',shell=True))

def getLabStatus(l):
    try:
        return get('pod -l app=jupyter-'+l.__str__()).get('items')[0].get('status').get('containerStatuses')[0]
    except:
        return {'ready':False}

def getLab(l):
    return get('pod -l app=jupyter-'+l.__str__()).get('items')[0]

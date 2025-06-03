import subprocess
import os
import yaml
import base64

from rest_framework.authtoken.models import Token

#GENERAL STUFF
ROOT_PATH = '../templates/'
K = 'minikube kubectl -- --namespace=hysealab '
VOL_TEMPLATE = '''        - name: hysea-lab-%(LAB_ID)s-pv
          mountPath: "/home/jovyan/%(EMAIL)s"
'''

def labUrl(user,token):
    #return 'http://hysea-lab-'+user+'-svc.hysealab.cluster.local:'+str(30000+int(user))+'/token?='+token
    return 'http://$(minikube ip):'+str(30000+int(user))+'/token?='+token

def deploy(filename,env):
    for x in env:
        os.system('echo $'+x)
        os.putenv(x,env[x])
    return yaml.full_load(subprocess.check_output('envsubst < '+ROOT_PATH+filename+' | '+K+' apply -o yaml -f -', shell=True))

def get(object):
    return yaml.full_load(subprocess.check_output(K+" get "+object+' -o yaml',shell=True))

def delete(object):
    return {'name':subprocess.check_output(K+" delete "+object+' -o name',shell=True)}


#LAB FUNCTIONS
def volParser(id,email):
    return VOL_TEMPLATE % {'LAB_ID':id,'EMAIL':email}

def volumeListParser(id_list):
    output = ''
    for id in id_list:
        output += volParser(id,Token.objects.get(key=id).user.__str__())
    return output

def createLab(id,token,email,invitation_list):
    env = {
        "LAB_ID":id,
        "USER_TOKEN":token,
        "EMAIL":email,
        "VOL_LIST":volumeListParser(invitation_list)
    }
    return deploy('lab.yaml',env)
def getLabStatus(l):
    try:
        return get('pod -l app=hysea-lab-'+l.__str__()).get('items')[0].get('status').get('containerStatuses')[0]
    except:
        return {'ready':False}

def getLab(l):
    return get('pod -l app=hysea-lab-'+l.__str__()).get('items')[0]

def deleteLab(l):
    return delete('deployment.apps/hysea-lab-'+l.__str__())


#SERVICE FUNCTIONS
def createSvc(id):
    env = {
        'LAB_ID':id,
        'NODE_PORT':str(30000+int(id))
        }
    return deploy('svc.yaml',env)
    #return subprocess.check_output(K+' expose deployment/hysea-lab-'+id+' --type="NodePort" --name=hysea-lab-'+id+'-svc -o yaml', shell=True)

def deleteSvc(id):
    return delete('hysea-lab-'+id+'-svc')
    #return subprocess.check_output(K+' expose deployment/hysea-lab-'+id+' --type="NodePort" --name=hysea-lab-'+id+'-svc -o yaml', shell=True)

def getSvcStatus(user,token):
    try:
        return subprocess.check_output('curl '+labUrl(user,token) , shell=True)
    except:
        return {'ready':False}


#TOKEN FUNCTIONS
def createSecretToken(user,token):
    env = {
        'USER_ID':str(user),
        'USER_TOKEN':base64.b64encode(token.encode("ascii")).decode("ascii")
    }
    return deploy('secret.yaml',env)

def deleteSecretToken(user):
    try:
        return delete('secret user-'+str(user))
    except:
        return {'warning':'no secret has been found'}


#PVC FUNCTIONS
def createPVC(id):
    env = {
        'VOL_ID':str(id)
    }
    return deploy('pvc.yaml',env)

def deletePVC(user):
    try:
        return delete('pvc hysea-lab-'+str(user)+'-pvc')
    except:
        return {'warning':'no secret has been found'}

def checkPVC(id):
    try:
        return get('pvc hysea-lab-'+id+'-pvc').get('status').get('phase')
    except:
        return None


#PV functions
def createPV(id,email):
    env = {
        'VOL_ID':str(id),
        'EMAIL':email
    }
    return deploy('pv.yaml',env)

def checkPV(id):
    try:
        return get('pv hysea-lab-'+id+'-pv').get('status')
    except:
        return None

def getPV(id):
    try:
        return get('pv hysea-lab-'+id+'-pv')
    except:
        return None

def deletePV(user):
    try:
        return delete('pv hysea-lab-'+str(user)+'-pv')
    except:
        return {'warning':'no secret has been found'}
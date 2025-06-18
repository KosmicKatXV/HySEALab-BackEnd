import subprocess
import os
import yaml
import base64
import k8s.settings as s

#GENERAL STUFF
ROOT_PATH = '../templates/'
K = 'minikube kubectl -- --namespace=hysealab '
PV_TEMPLATE = '''        - name: hysea-lab-%(LAB_ID)s-pv
          mountPath: "/home/jovyan/%(EMAIL)s"
'''
PVC_TEMPLATE = '''      - name: hysea-lab-%(LAB_ID)s-pv
        persistentVolumeClaim:
          claimName: hysea-lab-%(LAB_ID)s-pvc
'''
TOOLBOX_PV_TEMPLATE = '''        - name: toolbox-pv
          mountPath: "/home/jovyan/toolbox"
'''
TOOLBOX_PVC_TEMPLATE = '''      - name: toolbox-pv
        persistentVolumeClaim:
          claimName: toolbox-pvc
'''

def labUrl(ip,user,token):
    #return 'http://hysea-lab-'+user+'-svc.hysealab.cluster.local:'+str(30000+int(user))+'/token?='+token
    return 'http://'+ip+':'+str(30000+int(user))+'/lab?token='+token

def deploy(filename,env):
    for x in env:
        os.system('echo $'+x)
        os.putenv(x,env[x])
    os.system('envsubst < '+ROOT_PATH+filename)
    return yaml.full_load(subprocess.check_output('envsubst < '+ROOT_PATH+filename+' | '+K+' apply -o yaml -f -', shell=True))

def get(object):
    return yaml.full_load(subprocess.check_output(K+" get "+object+' -o yaml',shell=True))

def delete(object):
    return {'name':subprocess.check_output(K+" delete "+object+' -o name',shell=True)}


#LAB FUNCTIONS
def PVParser(id,email):
    return PV_TEMPLATE % {'LAB_ID':id,'EMAIL':email}

def PVCParser(id):
    return PVC_TEMPLATE % {'LAB_ID':id}

def PVListParser(invitation_list):
    output = ''
    for i in invitation_list:
        output += PVParser(i.get('id'),i.get('email'))
    return output

def PVCListParser(invitation_list):
    output = ''
    for i in invitation_list:
        output += PVCParser(i.get('id'))
    return output

def createLab(id,token,email,invitation_list):
    print(s.TOOLBOX_ENABLED)
    env = {
        "LAB_ID":id,
        "USER_TOKEN":token,
        "EMAIL":email,
        "PV_LIST":PVListParser(invitation_list),
        "PVC_LIST":PVCListParser(invitation_list),
        "TOOLBOX_PV": TOOLBOX_PV_TEMPLATE if s.TOOLBOX_ENABLED else "",
        "TOOLBOX_PVC": TOOLBOX_PVC_TEMPLATE if s.TOOLBOX_ENABLED else ""
    }
    return deploy('lab.yaml',env)

def getLabStatus(l):
    try:
        return get('pod -l app=hysea-lab-'+l.__str__()).get('items')[0].get('status').get('containerStatuses')[0]
    except:
        return {'ready':False}

def getLab(id,token):
    output = get('pod -l app=hysea-lab-'+id).get('items')[0]
    ip = output.get('status').get('hostIP') 
    output.update({'url':labUrl(ip,id,token)})
    return output

def deleteLab(l):
    try:
        return delete('deployment.apps/hysea-lab-'+l.__str__())
    except:
        return {'warning':'no lab found'}

#SERVICE FUNCTIONS
def createSvc(id):
    env = {
        'LAB_ID':id,
        'NODE_PORT':str(30000+int(id))
        }
    return deploy('svc.yaml',env)
    #return subprocess.check_output(K+' expose deployment/hysea-lab-'+id+' --type="NodePort" --name=hysea-lab-'+id+'-svc -o yaml', shell=True)

def deleteSvc(id):
    return delete('svc hysea-lab-'+id+'-svc')
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
def createPVC(id,squota):
    env = {
        'VOL_ID':str(id),
        'SPACE_QUOTA':squota
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

#TOOLBOX FUNCTIONS
def createToolBoxPVC():
    env = []
    print(deploy('toolbox-pvc.yaml',env))

def deleteToolBoxPVC():
    print(delete('pvc toolbox-pvc'))

def createToolBoxPV():
    env = []
    print(deploy('toolbox-pv.yaml',env))

def deleteToolBoxPV():
    print(delete('pv toolbox-pv'))

def createGitSyncPod(url):
    env = {
        "REPO_URL":url
    }
    print(deploy('git-sync.yaml',env))

def deleteGitSyncPod(l):
    print(delete('deployment.apps/git-sync'))
import k8s.k8s as k
import k8s.settings as s

if s.TOOLBOX_ENABLED:
    #Create deployment
    k.createGitSyncPod(s.TOOLBOX_URL)
    #Create PVC
    k.createToolBoxPVC()
    #Create PV
    k.createToolBoxPV()
else:
   #Delete deployment
   k.deleteGitSyncPod()
   #Delete PVC
   k.deleteToolBoxPVC()
   #Delete PV
   k.deleteToolBoxPV()
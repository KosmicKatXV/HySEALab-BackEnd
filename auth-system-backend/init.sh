rm -f db.sqlite3

#nuke option. Comment
#minikube delete --all
#sudo systemctl start docker
#minikube start

minikube kubectl -- --namespace=hysealab delete all --all
minikube kubectl -- --namespace=hysealab delete pvc --all
minikube kubectl -- --namespace=hysealab delete pv --all
minikube kubectl delete namespace hysealab
minikube kubectl create namespace hysealab

python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py shell < k8s/toolbox.py
python manage.py createsuperuser

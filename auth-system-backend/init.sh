rm -f db.sqlite3

minikube kubectl -- --namespace=hysealab delete pv --all
minikube kubectl delete namespace hysealab
minikube kubectl create namespace hysealab

python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py createsuperuser
redis-server --daemonize yes --port 4444

python3 worker.py & 

cd .. 

if [ -z ${PORT+x} ]; 
    then
        gunicorn wsgi:app --reload   --bind 0.0.0.0:5000; 
    else  
        gunicorn wsgi:app --reload   --bind 0.0.0.0:$PORT; 
fi

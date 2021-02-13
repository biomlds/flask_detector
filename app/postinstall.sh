redis-server --daemonize yes --port 4444

python3 worker.py & 

cd .. 

if [ -z ${PORT+x} ]; 
    then
        export SECRET_KEY=DBuCWzKpaX4Qiin7Z4BYxHUO6HkBR75BcbPxJdYJbbkyn5V06
        gunicorn wsgi:app --reload   --bind 0.0.0.0:5000; 
    else  
        gunicorn wsgi:app --reload   --bind 0.0.0.0:$PORT; 
fi

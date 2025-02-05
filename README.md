1) Before running container need set permissions to run.sh script

   -`chmod +x containers/run.sh `


2) Make migrations inside container
   
   -`docker-compose exec api bash`

   -`python3 manage.py migrate`


3) Run & build docker
  
   -`docker-compose up --build`
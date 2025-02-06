1) Run & build docker
  
   -`docker-compose up --build`


2) Make migrations inside container
   
   -`docker-compose exec api bash`

   -`python3 manage.py migrate`


Rest Api Client (CoinMarketCap & Blockchair)
1. Credentials saving in db (table `ExternalCredentials`) - basic (test) credentials was writing during migrations
2. Credentials has been changed in admin-panel
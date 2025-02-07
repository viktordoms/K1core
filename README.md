1) Run & build docker
  
   -`docker-compose up --build`


2) Make migrations inside container
   
   -`docker-compose exec admin bash`

   -`python3 manage.py migrate`


3) Need to restart containers


Rest Api Client (CoinMarketCap & Blockchair)
1. Credentials saving in db (table `ExternalCredentials`) - basic (test) credentials was writing during migrations
2. Credentials has been changed in admin-panel

URLs:
1) `/admin` - Django URLs
2) `/api` - FastApi URLs  (`'headers': {'API-Key': '.....'}`)

Users:

`When user finished registration - his account is not active `

`Admin must activate in admin-panel his account`

Configs:
1) File`/K1core/local_conf.py.excemple` need to rename `/K1core/local_conf.py`  
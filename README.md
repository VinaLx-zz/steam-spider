# steam-spider
### Brief

crawl game informations from steam including like rates, number of review people, genres etc.

It's merely runnable now, not quite usable :P

### Dependency

- python3.x
  - pymysql
  - beautifulsoup4
  - requests
- mysql

### Usage

- Modify username, password etc. in  `path/to/steam-spider/src/steamspider/config-files/db.json` 

- 
```bash
   cd src/steamspider/database
   python3 initdb.py
   cd ..
   python3 steam.py
```

- wait...

- mysql and query



### TODO

- User interface instead of sql query directly
- More Infomations such as reviews and prices
- More flexible way to crawl informations
- ...

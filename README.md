# TestFBK

This is version of test for FBK

## For testing:

1. Build and run app
```
   git clone https://github.com/daria-maslovskaya/TestFBK.git
   cd TestFBK
   docker-compose up -d 
```

2. Try POST curl requests
```
   # returns success
   curl -X POST http://localhost:8080/region/1?"name"="Taras"&"lastname"="Lojkin"&"age"=33&"email"="test@mail.com"
   
   #returns error "Connection refused"
   curl -X POST http://localhost:5000/rgion/1?"name"="Taras"&"lastname"="Lojkin"&"age"=33&"email"="test@mail.com"
```

3. Try GET curl requests
```
   # both return error
   curl http://localhost:8080/region/1
   curl http://localhost:5000/region/1
```

4. Check that DB contain new data
```
   # connect to db
   docker exec -it db_fbk bash
   psql postgresql://testFBK:testFBK@db_fbk:5432/testFBK
   # check list of dbs
   testFBK=# \l
   # check list of tables
   testFBK=# \dt
   # check that initial samples loaded
   testFBK=# select * from regions;
   # check that new citizen was added to table
   testFBK=# select * from citizens;
```

Links:
- https://habr.com/ru/company/skillbox/blog/464705/
- https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/#gunicorn
- https://docs.sqlalchemy.org/en/13/index.html

PS: I started with another variant, but read interesting example with gunicorn and wanted to try it
    So, I put deprecated variant in archive/ folder

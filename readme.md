#blog project

blog project made using MS SQL DB, Fastapi backend, React TS frontend

1. Install Docker.
2. Set up .env file in ./blog directory:
    DATABASE_LOGIN=SA <br />
    #If u want to change password, it must has 8 symbols, at leat 1 lower case, 1 upper case, 1 number and 1 special symbol. <br />
    #If u changing, change it in ./blog/docker/driver/odbc.ini too. <br />
    DATABASE_PASSWORD=SuperPASSW0RD! <br />
    DATABASE_SERVER=mssql-server <br />
    DATABASE_PORT=14333 <br />
    DATABASE_NAME=BLOG <br />

    FASTAPI_DOMAIN=http://127.0.0.1:14555 <br />
    FASTAPI_PORT=14555 <br />

    REACT_DOMAIN=http://127.0.0.1:14777 <br />
    REACT_LOCALHOST_DOMAIN=http://localhost:14777 <br />
    REACT_PORT=14777 <br />

    #You can easy change your pepper and jwt secret. It used for hash and encode password to db. <br /> 
    PEPPER=MakeItStrong <br />
    JWT_SECRET=MakeItStrong <br />
    JWT_ALGORITHM=HS256 <br />
3. Open CMD ang go to BLOG folder location.
4. Run "docker-compose up -d" and wait for 2 min for initialization database.
5. Press ctrl+z, run docker-compose down; docker rmi blog-python blog-react.
6. Change in blog/docker/python/Dockerfile last string to "CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "14555"]".
7. Run "docker-compose up -d".
8. Now u can go to http://127.0.0.1:14777 or http://localhost:14777 and use the app.
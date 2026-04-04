# Postgres docker start command
- docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres:16-alpine

# pgadminer for browser use of postgresql
host.docker.internal
System	 :PostgreSQL
Server	:host.docker.internal
Username	:postgres
Password	:mysecretpassword
Database	:postgres


# docker compose


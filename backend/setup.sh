# Get postgres for local development
docker run -p 5432:5432 --name postgreslocal -e POSTGRES_PASSWORD=mysecretpassword -d postgres

# Get pgadmin
docker pull dpage/pgadmin4
docker run -p 80:80 -e 'PGADMIN_DEFAULT_EMAIL=user@domain.com'-e 'PGADMIN_DEFAULT_PASSWORD=SuperSecret' -d dpage/pgadmin4



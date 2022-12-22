# Deploy micro-services group (data_gathering app and mysql database) with docker

## For deploy micro services group :

```
docker-compose up -d --build
```

## To enter in bash of database docker :

```
docker exec -it fleet_database bash
```

## Creating database dumps without data :

```
docker exec fleet_database sh -c 'exec mysqldump -u root -p"$MYSQL_ROOT_PASSWORD" fleet --no-data' > ./fleet_databases_struct.sql
```

## Creating database dumps :

```
docker exec fleet_database sh -c 'exec mysqldump -u root -p"$MYSQL_ROOT_PASSWORD" fleet' > ./fleet_databases.sql
```

## Restoring data from dump files :

```
docker exec -i fleet_database sh -c 'exec mysql -u root -p"$MYSQL_ROOT_PASSWORD" fleet' < ./fleet_databases.sql

```

## Run test of data_gathering app :

```
docker exec -it data_gathering_service pytest . -s
```

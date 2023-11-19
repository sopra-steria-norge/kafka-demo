# Kafka Demo

So the following [Conflunet Components](https://www.confluent.io/) are in this Demo.

- [Kafka with KRaft](https://docs.confluent.io/kafka/overview.html) (No zookeper needed any more)
- [Schema Registry](https://docs.confluent.io/platform/current/schema-registry/index.html)
- [Connect](https://docs.confluent.io/platform/current/connect/index.html#:~:text=%C2%B6,search%20indexes%2C%20and%20file%20systems.)
- [ksqlDB](https://ksqldb.io/) - [Confluent Page](https://docs.confluent.io/platform/current/streams-ksql.html)
- [Control Center](https://docs.confluent.io/platform/current/control-center/index.html)

The demo is based on two applications where one is written in Python and one in .NET. The REST API part is the .NET application,
where F1 sessions are requested. Then the Python application handles the request one at a time and generates different session
data to Kafka topics.

The python uses as a basis FastAPI and is written to generate data concurently. This was mostly for my self to test how it would be to develope in python and use
the Confluent SDK in an async/await world.

The .NET application is just has just 3 simple endpoints to request data, and two other REST methods to get the different ID for multiple requests, and get the statuses
from those requests.

# How TO

## 1. Start up the Confluent Components

Start up the Components with docker compose with the following commands. This will start all the components and show the logs in the console window.

The force recreate is to just show that you can easly start with new instances if you want to start all over again and delete excisting data.

```shell
docker-compose up --force-recreate -V
```

If on a Unix/Linux system you can also use `make`:

```shell
make start-confluent
```

## 2. Test and famaliarize with the instances

When the components are started up they can be reached in an brower with the following URLs. The connect and ksqlDB will only show some info, tough they do have some REST APIs, or they can be seen and used from the Control Center.
Since connect is also downloading and installing several connectors it can take some time before it is available.

- [Control Center](http://localhost:9021/)
- [Schema Registry](http://localhost:8081) - To se schemas use [Schemas](http://localhost:8081/schemas)
- [Connect](http://localhost:8083/)
- [ksqlDB](http://localhost:8088)

## 3. Start up the python instance

This will build an docker image and start an python application that will handle requests for F1 sessions.
Tough it is programmed to only handle one request at a time, so it will pause the consumption of requests when handling an request.

Start the F1 request handler by running:

```shell
docker-compose -f docker-compose.f1-1.yaml up
```

if on a Unix/Linux system you can also use `make`:

```shell
make start-f1-1:
```

When the backend is up and running you will see that in final parts of the log it will say it has been assigned two partitions.
Since it can only handle 1 request at a time we can double the request handling by starting one more request processor.

## 4. Start another F1 request processor

Start another processor and see that the partitions is beeing split between the two in a round robin fashion:

```shell
docker-compose -f docker-compose.f1-2.yaml up
```

if on a Unix/Linux you can also use `make`:

```shell
make start-f1-2
```

In the logs when the new processor has been started you will see that it get one partition assigned and that the first will get its partitions revoked and then get the other partition.
You can then stop nr1 in step 3 and start it again to see that Kafka rebalances the partitions between the two processors as the start and stop.

## 5. Start the .NET API

Now the API can be started by running the following command. When the container is running the API can be reached from [http://localhost:8080/docs](http://localhost:8080/docs)

```shell
docker-compose -f docker-compose.api.yaml up --build
```

if on a Unix/Linux you can also use `make`:

```shell
make start-api
```

## 6. From here request some formula one data

Use the API to send an request and see that one of the F1 processor picks the request up and starts to generate data and can be seen on the different topics from the Control Center.

# Kafka Demo

So the following [Conflunet Components](https://www.confluent.io/) are in this Demo.

- [Kafka with KRaft](https://docs.confluent.io/kafka/overview.html) (No zookeper needed any more)
- [Schema Registry](https://docs.confluent.io/platform/current/schema-registry/index.html)
- [Connect](https://docs.confluent.io/platform/current/connect/index.html#:~:text=%C2%B6,search%20indexes%2C%20and%20file%20systems.)
- [ksqlDB](https://ksqldb.io/) - [Confluent Page](https://docs.confluent.io/platform/current/streams-ksql.html)
- [Control Center](https://docs.confluent.io/platform/current/control-center/index.html)

The demo is based on two applications where 1 is written in Python and one in .NET. The REST API part is the .NET application,
where F1 sessions are requested. Then the Python application handles the request one at a time and generates different session
data to Kafka topics.

1. Start up the Components with docker compose with the following commands. This will start of all the components and show the logs in the console window.

```shell
docker-compose up --force-recreate -V
```

If on a Unix/Linux system you can also use:

```shell
make start-confluent
```

2. When the components are booted up they can be reached in an brower with the following URLs. The connect and ksqlDB will only show some info, tough they do have some REST APIs, or they can be seen and used from the Control Center.

- [Control Center](http://localhost:9021/)
- [Schema Registry](http://localhost:8081) - To se schemas use [Schemas](http://localhost:8081/schemas)
- [Connect](http://localhost:8083/)
- [ksqlDB](http://localhost:8088)

3. Start the F1 Request Handler by running. This will build an docker image and start an python application that will handle requests for F1 sessions.
Tough it is programmed to only handle one request at a time, so it will pause the consumption of requests when handling an order.

When the F1-1 has been started

```shell
docker-compose -f docker-compose.f1-1.yaml up
```

if on a Unix/Linux system you can also use:

```shell
make start-f1-1:
```

When the backend is up and running you will see that in final parts of the log it will says it has been assigned two partitions.
Since it can only handle 1 request at a time we can double the request handling by starting one more processor.

4. Start another processor and see the partitions beeing split between the two:

```shell
docker-compose -f docker-compose.f1-2.yaml up
```

if on a Unix/Linux you can also use:

```shell
make start-f1-2
```

see the logs when the new processor has been started. You can then stop nr1 in step 3 and start it again to see that Kafka
rebalances the partitions between the two processors.

5. Now the API can be started by running the following command. When the container is running the API can be reached from
http://localhost:8080/docs

```shell
docker-compose -f docker-compose.api.yaml up --build
```

if on a Unix/Linux you can also use:

```shell
make start-api
```

# Tutorial

start-confluent:
	docker-compose up --force-recreate -V

start-f1-1:
	docker-compose -f docker-compose.f1-1.yaml up --build

start-f1-2:
	docker-compose -f docker-compose.f1-2.yaml up

start-api:
	docker-compose -f docker-compose.api.yaml up --build


# Utils

kafka-ui-start:
	docker run --rm -it --name kafka-ui -p 8080:8080 -e DYNAMIC_CONFIG_ENABLED=true provectuslabs/kafka-ui

kafka-ui-stop:
	docker stop kafka-ui

kind-start:
	kind create cluster

kind-destroy:
	kind delete cluster

protoc-python:
	protoc -I=. --python_out="src/f1" --pyi_out="src/f1" ./protobuf/*.proto

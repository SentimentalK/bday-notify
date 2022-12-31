build:
	docker build . --network=host -t notify
run:
	docker run --net=host --name notify notify
rerun:
	docker restart $$(docker ps -a --filter "name=notify" -q)
clean:
	docker rmi $$(docker images --filter "dangling=true" -q --no-trunc)
stop:
	docker stop $$(docker ps -a --filter "name=notify" -q)
	docker rm $$(docker ps -a --filter "name=notify" -q)

image = arthurnap24/cpp_box:1.0.0.0
container = $(image)
bash = /bin/bash
dir_host = .
dir_container = /ArthurCode

# Remove intermediate containers after successful build.
build:
	docker build --rm --tag $(image) .

# Run the Docker container and set /versateach/ dir as urrent working directory.
run:
	docker run -it --privileged -v $(shell pwd)/Sources:$(dir_container) $(container) $(bash)

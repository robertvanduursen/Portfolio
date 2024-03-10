image_name="brummen_api"

io: ## build an image for local use
	docker build -t $(image_name) .
	aplay klaar.wav

run:
	docker run --rm -it $(image_name) bash
	docker run -p 5000:5000 my_image
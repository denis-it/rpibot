#!/bin/bash

function build {
	docker build -t denis-it/rpibot .
}

COMMAND=${1:-run}

case $COMMAND in
	run)
	build
	docker run --rm --name rpibot denis-it/rpibot rpibot.py
	;;

	sh)
	build
	docker run -it --rm --name rpibot --entrypoint /bin/bash denis-it/rpibot
	;;

	*)
	echo "Unknown command: $COMMAND" >&2
	echo "Usage: $0 [command]" >&2
	echo "	run     run bot (default)" >&2
	echo "	sh      run a shell in the container" >&2
	exit 1
	;;
esac

run:
	python3 run.py

run-docker: clean
	docker pull brendonng/createmesimulation:simulation-app
	docker run -it -v `pwd`:/simulation --name=createmesimulation brendonng/createmesimulation:simulation-app python3 /simulation/run.py

clean:
	docker rm createmesimulation
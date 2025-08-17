Byung Ho Cho
cse304
Compiler Design: Phase 1

For this sub-project of implementing the lexical analyzer, 
I've used python3 with ubuntu serving as the base image. 

Building the environment
docker build -t lexical-analyzer 

To run the code with the test file 
	# navigate to interactive shell
	docker run -it lexical-analyzer /bin/bash
	# within the interactive shell 
	python3 main.py <filename>
	ex) python3 main.py test.rsc
Byung Ho Cho
cse304
Compiler Design: Phase 3

For this sub-project of implementing the parser combined with lexer, 
I've used python3 with ubuntu serving as the base image. 

Building the environment
docker build -t rascl-parser .

To run the code with the test file 
	# navigate to interactive shell
	docker run -it rascl-parser /bin/bash
	# within the interactive shell (running the test cases code)
	python3 parser_main.py <rsc file of your choice>
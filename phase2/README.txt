Byung Ho Cho
cse304
Compiler Design: Phase 2

For this sub-project of implementing the symbol table manger, 
I've used python3 with ubuntu serving as the base image. 

Building the environment
docker build -t symbol-table-manager .

To run the code with the test file 
	# navigate to interactive shell
	docker run -it symbol-table-manager /bin/bash
	# within the interactive shell (running the test cases code)
	python3 testDriver.py 
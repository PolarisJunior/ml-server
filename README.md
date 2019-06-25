# ml-server
Socket server for running machine learning algorithms. 

The client opens a TCP connection to the server and
runs requests in the following format, all numbers
are in big endian

4 bytes denote the algorithm
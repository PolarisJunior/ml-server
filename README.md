# ml-server
TCP Server for running machine learning and AI algorithms on
arbitrary datasets

The client opens a TCP connection to the server and sends a request with a specific protocol to the server, with the data to be processed at the end of the request payload. The server will then process the data with the specified algorithms, and return the result. The protocol is described below.

First note that all integers and floats are stored in big-endian

The first 4 bytes is an integer denoting the entire length in bytes of the request, including these 4 bytes themselves. 

The next 4 bytes is an integer representing the algo_id (algorithm id) to be run. 

Next, an arbitrarily long sequence of (argument name, value) pairs. That is, the argument name is a 4 byte integer for the length of the string, followed by the string encoded in UTF-8. The argument name is followed by a value which is typically a 4 byte numeric type. The list of arguments is terminated once it receives the 4 byte integer 0 instead of an argument name. 

Lastly, the data to be processed is simply a sequence of 4 byte floats. The data will be interpreted and processed by the server based on the arguments previously provided. For example, ML typically deals with vectors rather than individual floats, so
providing the pair (dims, 3) will tell the server to interpret each 3 consecutive floats as one vector.

Current Available Algorithms (In the ml_modules folder)
# Machine Learning #
KMeans

# AI #

To add new algorithms, a class extending MlBase must be added under the **ml_modules** folder, and the class member variable algo_id must be set to some integer. Only classes under this folder will be detected as a valid algorithm

TODO
* Allow creating a processing pipeline by specifying multiple algorithms to run sequentially
* Instead of reading the client message entirely to memory, stream the data
* Use strings as identifiers for algorithms rather than arbitrary integers
* Allow subdirectories in the ml_modules folder
* Create a document specifying the arguments for various algorithms
* Allow arguments to have strings as values
* Allow arguments to have floats as values
* Possibly have a way to define arguments to algorithms in a way such that the server determines how to interpret the argument value as a float or integer. That is, creating a mapping from argument names to types
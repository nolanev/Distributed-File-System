Student: Eva Nolan
Student Number: 14335043

A basic distributed file system written in Python using sockets. The system includes a directory server, a caching server and a locking server


Client.py

The client server allows for testing of the system. It is set up to request access to first a cached file and second a not cached file. It asks the lock server for a lock on a file. This is done through polling. The client polls the lock server until the file is free. When the lock request is granted the client sends a request to the cache server. When the client is finished with the file it lets the lock server know and the file is unlocked.

Lock.py

The lock server grants and denies file requests from the client depending on whether or not the file is currently in use by another client. When access to a file is granted the file is added to the server locked list and any other request for that file will be denied. When a client sends a finished message, the server removes the file from its locked list

Cache.py

The cache server responds to a request from the client to find a file. If the file is cached locally in the cached files folder (standing in for an actual database) it returns the contents of the file to the client. If the file is not cached locally the cache server requests the file from the directory server. It sends on the returned file to the client and caches it file for use next time it is requested.

Server.py

The directory server is only called when the file is not saved in the local cache. The cache server sends a request to the directory server and the directory server checks if the file is present in the database (represented by a DB folder). It responds with the contents of the file which is then saved in the cache


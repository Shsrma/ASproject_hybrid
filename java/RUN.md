Java microservice (lightweight)
---------------------------------
This microservice uses the built-in com.sun.net.httpserver package (requires JDK 8+).
To compile and run:

javac -d out src/main/java/com/blocksharecloud/*.java
java -cp out com.blocksharecloud.Main

It will listen on http://127.0.0.1:9000
Endpoints:
- POST /verify  (JSON body) -> verifies/echos block data
- GET /timezone?region=Asia/Kolkata -> returns timezone and datetime
- GET /translate?lang=hi&text=Hello -> pseudo-translation

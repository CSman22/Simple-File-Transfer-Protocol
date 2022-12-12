# Network Application - A Simple File Transfer Service

### How to run the file

Use an IDE of your choice with Python version 3.10.9 or greater (Recommended).
In the following tutorial I used Visual Studio Code as the IDE of choice.

1. After unzipping the file open the source code in VS Code.
2. Open two terminals side by side each other
3. Make sure the directory of both terminals is to the src.
   If not change directory with the following command `cd src`
4. Run the server with the following command `python server.py 127.0.0.1 80 1`
5. Run the client with the following command `python client.py 127.0.0.1 80 1`
    > Server Address: 127.0.0.1
    > Port Number: 80
    > Debug Mode: 1 ON, anything else OFF

### Examples at the client Side

All the files at the client side are placed in the `ClientFolder`.
All the files at the Server side are placed in the `ServerFolder`.
You can insert different files into any of these folders and run the program.
The following are examples of running the program.

```
    	Help                            | Retrieve the user commands
	Get girl.jpg                    | Download a file from the server folder
	Put req.pdf                     | Upload a file to the server folder
	Change req.pdf requirement.pdf  | Change filename in the server folder
	err test                        | Scenario of a wrong input
	Bye                             | Close client connection
```

# In a second moment I will make new commands
# to hide these, with a proper helper, or maybe makefile?


# Start the server
python server.py

# Start the client
python client.py ../mcp-server-snap/server.py

# Start the inspector, run in the directory of the server and then click start
mcp-inspector python server.py
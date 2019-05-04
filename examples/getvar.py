from jsonrpcclient.http_client import HTTPClient
from jsonrpcclient.request import Request


client = HTTPClient('http://localhost:5000')
myvar = client.send(Request('Getvar',channel="DAHDI/1-1",variable="trunk"))
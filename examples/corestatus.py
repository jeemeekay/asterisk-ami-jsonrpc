from jsonrpcclient.http_client import HTTPClient
from jsonrpcclient.request import Request


client = HTTPClient('http://localhost:5000')
client.send(Request('CoreStatus'))
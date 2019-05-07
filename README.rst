##################################################################################################
JSONRPC Server that exposes Asterisk AMI Actions as jsonrpc http requests
##################################################################################################


==========
Python 3.x
==========

The server specifically works with **Python 2.x**. You can not use it with Python 3.x. In future, will port library to Python 3.x

============
Installation
============

::

    pip install -r requirements.txt
    

=============
Configuration
=============

You need to modify asterisk-ami-jsonrpc.py with a manager user in Asterisk manager.conf
Currently in the python script, the default values for ASTUSER and ASTSECRET is 'admin' 
See below for more information regarding Asterisk manager configuration. 

http://www.asteriskdocs.org/en/3rd_Edition/asterisk-book-html-chunk/AMI-configuration.html



==================
Running the Server
==================


::

    ./asterisk-ami-jsonrpc.py
    

=============================
Python jsonrpc client example
=============================

.. code:: python

    #!/usr/bin/env python
    # coding: utf-8

    
    from jsonrpcclient.http_client import HTTPClient
    from jsonrpcclient.request import Request
    
    #To send AMI action CoreStatus to get Core status  
    client = HTTPClient('http://localhost:5000')
    client.send(Request('CoreStatus'))

This returns the core status from Asterisk as below: 

::
     
     --> {"jsonrpc": "2.0", "method": "CoreStatus", "id": 1}
     <-- {"jsonrpc": "2.0", "result": {"CoreStartupDate": "2019-05-04", "CoreReloadDate": "2019-05-04", "CoreStartupTime": "17:16:58", "CoreCurrentCalls": "0", "ActionID": "457740", "CoreReloadTime": "17:16:58"}, "id": 1} (200 OK)





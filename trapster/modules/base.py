import asyncio
import json
import time
import datetime
from typing import Optional

# https://svn.nmap.org/nmap/nmap-service-probes

class ProtocolError(Exception):
    pass

class UnsupportedVersion(Exception):
    pass

class BaseProtocol(asyncio.Protocol):
    """common class to all protocol handler"""
    def __init__(self):
        self.protocol_name = "base"

    def connection_made(self, transport) -> None:
        self.transport = transport
        self.logger.log(self.protocol_name + "." + self.logger.CONNECTION, self.transport)
        self.transport.close()
        
    def data_received(self, data):
        self.logger.log(self.protocol_name + "." + self.logger.DATA, self.transport, data=data)
        self.transport.close()

    def connection_lost(self, exc: Optional[Exception]) -> None:
        self.transport.close()

class BaseHoneypot(object):
    """common class to all trapster instance"""

    def __init__(self, config, logger, bindaddr="0.0.0.0", **kwargs):
        self.port = config['port']
        self.bindaddr = bindaddr
        self.logger = logger 
        self.handler = BaseProtocol
        self.handler.logger = logger
        self.server = None
        self.task = None    

    async def start(self):
        # Start the server in a separate task
        loop = asyncio.get_running_loop()
        self.task = loop.create_task(self._start_server())
        return self.task
    
    async def _start_server(self):
        loop = asyncio.get_running_loop()
        try:
            self.server = await loop.create_server(self.handler, host=self.bindaddr, port=self.port)
            await self.server.serve_forever()
        except OSError as e:
            if e.errno == 98:
                print(f"Port {self.port} already in use on {self.bindaddr}")
                print(e)
        except asyncio.CancelledError:
            raise

    async def stop(self):
        self.task.cancel()
        try:
            await self.task
        except asyncio.CancelledError:
            print(f"Server {self.bindaddr}:{self.port} is cancelled now")

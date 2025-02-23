import socket
import struct
import asyncio
import logging
from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class ICMPPinger:
    def __init__(self):
        self.seq_number = 0
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        except PermissionError:
            logger.error("Raw socket creation requires root privileges")
            raise

    def create_packet(self) -> bytes:
        my_checksum = 0
        my_id = id(self) & 0xFFFF
        
        header = struct.pack('!BBHHH', 8, 0, my_checksum, my_id, self.seq_number)
        data = b'monitoring-ping'
        
        my_checksum = self._checksum(header + data)
        header = struct.pack('!BBHHH', 8, 0, my_checksum, my_id, self.seq_number)
        self.seq_number = (self.seq_number + 1) % 65536
        
        return header + data

    def _checksum(self, data: bytes) -> int:
        if len(data) % 2:
            data += b'\0'
        words = struct.unpack('!%dH' % (len(data) // 2), data)
        checksum = sum(words)
        checksum = (checksum >> 16) + (checksum & 0xFFFF)
        checksum += checksum >> 16
        return (~checksum & 0xFFFF)

    async def ping(self, host: str, timeout: float = settings.PING_TIMEOUT) -> bool:
        try:
            packet = self.create_packet()
            self.socket.sendto(packet, (host, 0))
            start_time = asyncio.get_event_loop().time()
            
            while asyncio.get_event_loop().time() - start_time < timeout:
                ready = await asyncio.get_event_loop().sock_recv(self.socket, 1024)
                if ready:
                    return True
                await asyncio.sleep(0.1)
            return False
        except Exception as e:
            logger.error(f"Error pinging {host}: {e}")
            return False
import asyncio
import logging
from datetime import datetime
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.host import Host
from app.services.ping import ICMPPinger
from app.services.email import EmailService
from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)
email_service = EmailService()

async def monitor_hosts():
    pinger = ICMPPinger()
    
    while True:
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(Host))
                hosts = result.scalars().all()
                
                for host in hosts:
                    current_status = await pinger.ping(host.host)
                    
                    if current_status != host.is_up:
                        host.is_up = current_status
                        host.last_check = datetime.now()
                        
                        if not current_status:
                            await email_service.send_email(
                                to_email=host.email,
                                subject=f"Host {host.host} is down!",
                                content=f"Your monitored host {host.host} is currently unreachable."
                            )
                
                await session.commit()
            
            await asyncio.sleep(settings.MONITOR_INTERVAL)
        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}")
            await asyncio.sleep(settings.MONITOR_INTERVAL)

async def start_monitor_task():
    asyncio.create_task(monitor_hosts())
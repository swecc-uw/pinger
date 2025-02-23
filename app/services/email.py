import logging
from typing import Optional
import aiohttp
from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.dev_mode = settings.DEV_MODE
        self.from_email = settings.EMAIL_FROM
        self.sendgrid_key = settings.SENDGRID_API_KEY

        if not self.dev_mode and not self.sendgrid_key:
            logger.warning("Production mode is enabled but SendGrid API key is not set!")

    async def send_email(
        self,
        to_email: str,
        subject: str,
        content: str,
    ) -> bool:
        try:
            if self.dev_mode:
                logger.info(f"""
                Would send email in production:
                To: {to_email}
                Subject: {subject}
                Content: {content}
                """)
                return True
            else:
                return await self._send_sendgrid_email(to_email, subject, content)
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False

    async def _send_sendgrid_email(self, to_email: str, subject: str, content: str) -> bool:
        if not self.sendgrid_key:
            logger.error("SendGrid API key not configured")
            return False

        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {
            "Authorization": f"Bearer {self.sendgrid_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "personalizations": [{
                "to": [{"email": to_email}]
            }],
            "from": {"email": self.from_email},
            "subject": subject,
            "content": [{
                "type": "text/html",
                "value": content
            }]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status in (200, 201, 202):
                    logger.info(f"Email sent to {to_email}")
                    return True
                else:
                    error_text = await response.text()
                    logger.error(f"SendGrid API error: {error_text}")
                    return False


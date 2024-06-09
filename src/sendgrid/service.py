from fastapi import HTTPException, status

import sendgrid
from config import (
    SENDGRID_API_KEY,
    SENDGRID_FORGOT_PASSWORD_TEMPLATE_ID,
    SENDGRID_FROM_EMAIL,
)
from sendgrid.helpers.mail import Mail


class SendgridService:
    def __init__(self):
        self.client = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        self.from_email = SENDGRID_FROM_EMAIL

    def send_email_with_template(
        self, template_id: str, to_email: str, data: dict
    ):
        message = Mail(
            from_email=self.from_email,
            to_emails=[to_email],
        )
        message.template_id = template_id
        message.dynamic_template_data = data

        try:
            self.client.send(message)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"sendgrid occurred error: {e.message}",
            )

    def send_reset_password_email(
        self, to_email: str, url: str, full_name: str
    ):
        self.send_email_with_template(
            template_id=SENDGRID_FORGOT_PASSWORD_TEMPLATE_ID,
            to_email=to_email,
            data={
                "full_name": full_name,
                "url": url,
            },
        )

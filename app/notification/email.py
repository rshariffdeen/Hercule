import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

from app.core import definitions
from app.core import values


def create_message(text, to_address, subject):
    msg = MIMEText(text)

    msg["Subject"] = subject
    msg["From"] = formataddr((f"{values.tool_name}", f"{values.tool_name.lower()}-noreply@comp.nus.edu.sg"))
    msg["To"] = to_address
    return msg


def send_message(text, subject=f"{values.tool_name} status update"):
    if not values.email_configuration[definitions.KEY_ENABLED]:
        return
    client = (
        smtplib.SMTP_SSL
        if values.email_configuration["ssl_from_start"]
        else smtplib.SMTP
    )
    username = values.email_configuration["username"]
    with client(values.email_configuration["host"]) as s:
        s.login(
            username,
            values.email_configuration["password"],
        )
        s.sendmail(
            username,
            [values.email_configuration["to"]],
            create_message(text, values.email_configuration["to"], subject).as_string(),
        )

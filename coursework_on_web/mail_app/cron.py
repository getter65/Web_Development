from config.settings import TIME_ZONE
from mail_app.management.commands.start_mailing import do_mailing
from mail_app.models import Mailing, MailingAttempt
from datetime import datetime, timedelta


def my_scheduled_job():

    to_send = False
    now = datetime.now()
    mailings = Mailing.objects.filter(status__in=[Mailing.STARTED, Mailing.CREATED])

    for mailing in mailings:
        if mailing.time.strftime("%H:%M") == now.strftime("%H:%M"):
            last_attempt = MailingAttempt.objects.filter(mailing=mailing.id).last()

            if not last_attempt:
                to_send = True
            else:
                from_last = now.date() - last_attempt.time.date()
                if mailing.frequency == Mailing.MONTHLY and from_last == timedelta(days=30) or mailing.frequency == Mailing.WEEKLY and from_last == timedelta(days=7) or mailing.frequency == Mailing.DAILY and from_last == timedelta(days=1):
                    to_send = True

        if to_send:
            do_mailing(mailing, mailing.id)

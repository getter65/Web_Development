from django.core.mail import send_mail
from django.core.management import BaseCommand

from config.settings import EMAIL_HOST_USER
from mail_app.models import Mailing, MailingAttempt


def do_mailing(mailing, pk):
    mailing.status = Mailing.STARTED
    mailing.save()

    print(f'Mailing {pk} has started.')

    try:
        recipients = mailing.recipient.all()
        rec_list = [rec.email for rec in recipients]
        result = send_mail(
            subject=mailing.message.topic,
            message=mailing.message.body,
            from_email=EMAIL_HOST_USER,
            recipient_list=rec_list,
            fail_silently=False
        )

        if result:
            mailing_attempt = MailingAttempt.objects.create(
                status=MailingAttempt.SUCCESS,
                answer=200,
                mailing_id=mailing.id
            )

            print(f'Mailing has been sent. Success mailing attempt {mailing_attempt.id} is created.')

        else:
            mailing_attempt = MailingAttempt.objects.create(
                status=MailingAttempt.FAIL,
                answer='Сообщение не отправлено (получателя нет либо указан неверный адрес почты)',
                mailing_id=mailing.id
            )

            print(f'Mailing has not been sent. Fail mailing attempt {mailing_attempt.id} is created.')

    except Exception as err:
        mailing_attempt = MailingAttempt.objects.create(
            status=MailingAttempt.FAIL,
            answer=err,
            mailing_id=mailing.id
        )

        print(f'Mailing has not been sent. Fail mailing attempt {mailing_attempt.id} is created.')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("args", metavar="mailing", nargs="+", help="")

    def handle(self, *args, **options):
        pk = args[0]
        mlng = Mailing.objects.filter(pk=pk).first()
        do_mailing(mlng, pk)

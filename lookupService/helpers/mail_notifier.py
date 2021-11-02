from django.core.mail import EmailMessage


def generate_completed_job_mail(recipient, job):
    email = EmailMessage(
        'MirMachine | Your job finished',
        'You are receiving this email because this address was registered to be notified ' +
        'when MirMachine job with id {job} is completed.\n\n The job is now complete and the results ' +
        'can be viewed at http://localhost:8000/job/{job}\n\n' +
        'If you did not request to be notified you may ignore this email.\n' +
        'Do not respond to this email, we will not receive it.\n' +
        'If you wish to contact us, see our website.\n\n' +
        'Regards,\nThe MirMachine Team'.format(job=job),
        'notifications@mirmachine.com',
        [recipient]
    )
    email.send()
    pass

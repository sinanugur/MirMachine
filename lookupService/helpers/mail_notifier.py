from django.core.mail import EmailMessage

def generate_completed_job_mail(recipient, job):
    email = EmailMessage(
        'MirMachine | Your job finished',
        'You are receiving this email because this mail address was registered to be notified ' +
        'when MirMachine job with id {job} is completed.\n\n The job is now complete and the results ' +
        'can be viewed at http://localhost:8000/job/{job}\n\n' +
        'If you did not request to be notified you may ignore this email.\n' +
        'Do not respond to this email, we will not receive it.\n' +
        'If you wish to contact us, see our website.\n\n' +
        'Regards,\nThe MirMachine Team'.format(job=job),
        'mirmachine@gmail.com',
        [recipient]
    )
    email.send()

def generate_job_initiated_mail(recipient, job):
    email = EmailMessage(
        'MirMachine | Your job has been submitted',
        'You are receiving this email because this mail address was registered to receive notifications ' +
        'regarding the status of the MirMachine job with id {job}.\n\n If you wish to view the progess of the job ' +
        'visit http://localhost:8000/job/{job}\n\nYou will also receive an email when the job is completed.\n\n' +
        'If you did not request to be notified you may ignore this email.\n' +
        'Do not respond to this email, we will not receive it.\n' +
        'If you wish to contact us, see our website.\n\n' +
        'Regards,\nThe MirMachine Team'.format(job=job),
        'mirmachine@gmail.com',
        [recipient]
    )
    email.send()


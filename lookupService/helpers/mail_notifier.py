from django.core.mail import EmailMessage
from django.conf import settings

def generate_completed_job_mail(recipient, job):
    email = EmailMessage(
        'MirMachine | Your job finished',
        'You are receiving this email because this mail address was registered to be notified ' +
        'when MirMachine job with id {job} is completed.\n\n The job is now complete and the results '.format(job=str(job.id)) +
        'can be viewed at https://www.mirmachine.org/job/{job}\n\n'.format(job=str(job.id)) +
        'If you did not request to be notified you may ignore this email.\n' +
        'Do not respond to this email, we will not receive it.\n' +
        'If you wish to contact us, see our website or contact us at support@mirmachine.org.\n\n' +
        'Regards,\nThe MirMachine Team',
        settings.EMAIL_USER,
        [recipient]
    )
    email.send(fail_silently=False)

def generate_job_initiated_mail(recipient, job):
    email = EmailMessage(
        'MirMachine | Your job has been initiated',
        'You are receiving this email because this mail address was registered to receive notifications ' +
        'regarding the status of the MirMachine job with id {job}.\n\n If you wish to view the progess of the job '.format(job=str(job.id)) +
        'visit https://www.mirmachine.org/job/{job}\n\nYou will also receive an email when the job is completed.\n\n'.format(job=str(job.id)) +
        'If you did not request to be notified you may ignore this email.\n' +
        'Do not respond to this email, we will not receive it.\n' +
        'If you wish to contact us, see our website or contact us at support@mirmachine.org.\n\n' +
        'Regards,\nThe MirMachine Team',
        settings.EMAIL_USER,
        [recipient]
    )
    email.send(fail_silently=False)

def generate_job_failed_mail(recipient, job):
    email = EmailMessage(
        'MirMachine | Your job failed',
        'You are receiving this email because this mail address was registered to receive notifications ' +
        'regarding the status of the MirMachine job with id {job}.\n\n'.format(job=str(job.id)) +
        'Unfortunately, your job has failed in the pipeline. Please check the parameters of your job.\n\n' +
        'If the error persists, please provide a description of the events and job ID to support@mirmachine.org\n\n' +
        'The job can be viewed at https://www.mirmachine.org/job/{job}\n\n'.format(job=str(job.id)) +
        'Do not respond to this email, we will not receive it.\n\n' +
        'Regards,\nThe MirMachine Team',
        settings.EMAIL_USER,
        [recipient]
    )
    email.send(fail_silently=True)


def manage_mail_notification(job, event):
    print('MAIL FUNCTION')
    address = job.mail_address
    if address == '':
        print('NO ADDRESS')
        return
    if event == 'initial':
        generate_job_initiated_mail(address, job)
    elif event == 'completed':
        generate_completed_job_mail(address, job)
        job.mail_address = ''
        job.save()
    elif event == 'halted':
        generate_job_failed_mail(address, job)
        job.mail_address = ''
        job.save()



from ..models import Job
from engine.scripts.mirmachine_args import run_mirmachine
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .maintainer import clean_up_temporary_files


def schedule_job():
    ongoing = Job.objects.filter(status='ongoing')
    # check if already job running
    if ongoing.exists():
        return
    queued = Job.objects.filter(status='queued').order_by('initiated')
    # check if queue is empty
    if not queued.exists():
        # clean_up_temporary_files()
        return
    next_in_line = queued[0]
    next_in_line.status = 'ongoing'
    next_in_line.save()
    announce_status_change(next_in_line)
    try:
        process, job_object = run_mirmachine(next_in_line)
        handle_job_end(process, job_object)
    except OSError:
        next_in_line.status = 'halted'
        next_in_line.save()
        announce_status_change(next_in_line)
    schedule_job()


def handle_job_end(process, job_object):
    if process.returncode != 0:
        job_object.status = 'halted'
    else:
        job_object.status = 'completed'
    job_object.save()
    announce_status_change(job_object)


def announce_status_change(job_object):
    layer = get_channel_layer('default')
    str_id = str(job_object.id)

    async_to_sync(layer.group_send)(
        str_id,
        {'type': 'status.update', 'status': job_object.status}
    )



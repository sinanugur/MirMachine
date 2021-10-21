

def validate_job_exists_and_complete(job_object):
    if not job_object:
        return {'message': 'Invalid job ID'}
    job_object = job_object[0]
    if job_object.status != 'completed':
        return {'message': 'This job has halted or is not yet complete'}
    return ''

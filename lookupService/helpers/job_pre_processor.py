import hashlib
import json
from lookupService.serializers import JobSerializer
from lookupService.helpers.ncbi_fetcher import get_fasta
from lookupService.models import Job


def process_form_data(request):
    serializer = JobSerializer(data=json.loads(request.POST.get('data')))
    updated_data = {}
    updated_data.update(serializer.initial_data)
    updated_data['user_cookie'] = request.COOKIES['csrftoken']
    forbidden = ['.', '/', '\\']
    if any(x in updated_data['species'] for x in forbidden):
        raise NameError
    if serializer.initial_data['mode'] == 'file':
        file = request.FILES.get('file')
        updated_data['data_file'] = file
        _list = []
        if serializer.initial_data['species'] == '':
            for chunk in file.chunks():
                decoded = chunk.decode('utf-8')
                lines = decoded.splitlines()
                updated_data['species'], i = extract_fasta_header(lines)
                break
    elif serializer.initial_data['mode'] == 'accNum':
        data = get_fasta(serializer.initial_data['data'])
        data = data.splitlines()
        i = 1
        if serializer.initial_data['species'] == '':
            updated_data['species'], i = extract_fasta_header(data)
        updated_data['data'] = ''.join(data[i:])
    updated_data['hash'] = hashlib.md5(serializer.initial_data['data'].encode()).hexdigest()
    updated_data['species'] = serializer.initial_data['species'].replace(' ', '_')
    updated_data['species'] = provide_unique_species(updated_data['species'])
    if updated_data['species'] == '':
        del updated_data['species']
    return JobSerializer(data=updated_data)


def extract_fasta_header(lines):
    i = 0
    header = ''
    next_line = lines[i]
    while next_line.startswith(('>', ';')):
        if i == 0:
            # cutoff header at 30 characters
            header = lines[i][1:31]
        i += 1
        next_line = lines[i]
    return header, i


def user_can_post(token):
    job_objects = Job.objects.filter(user_cookie=token)
    for job in job_objects:
        if job.status == 'ongoing' or job.status == 'queued':
            return False
    return True


def provide_unique_species(species):
    if Job.objects.filter(species=species).exists():
        i = 1
        new_species = species + str(i)
        while Job.objects.filter(species=new_species).exists():
            i += 1
            new_species = new_species[:-1] + str(i)
        return new_species
    return species

import hashlib
import json
from lookupService.serializers import JobSerializer


def process_form_data(request):
    serializer = JobSerializer(data=json.loads(request.POST.get('data')))
    if serializer.initial_data['mode'] == 'file':
        file = request.FILES.get('file')
        # TODO: parse header if fasta file
        for chunk in file.chunks():
            serializer.initial_data['data'] = serializer.initial_data['data'] + chunk.decode('utf-8')
    serializer.initial_data['hash'] = hashlib.md5(serializer.initial_data['data'].encode()).hexdigest()
    return serializer



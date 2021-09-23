import hashlib
import json
from lookupService.serializers import JobSerializer


def process_form_data(request):
    serializer = JobSerializer(data=json.loads(request.POST.get('data')))
    if serializer.initial_data['mode'] == 'file':
        file = request.FILES.get('file')
        fasta = file.name.endswith(('.fa', '.fasta'))
        parsed_header = False
        _list = []
        for chunk in file.chunks():
            decoded = chunk.decode('utf-8')
            if fasta and not parsed_header:
                if serializer.initial_data['species'] == '':
                    lines = decoded.splitlines()
                    serializer.initial_data['species'] = lines[0][1:]
                    _list.append(''.join(lines[1:]))
                parsed_header = True
                continue
            _list.append(decoded)
        serializer.initial_data['data'] = ''.join(_list)
    serializer.initial_data['hash'] = hashlib.md5(serializer.initial_data['data'].encode()).hexdigest()
    return serializer



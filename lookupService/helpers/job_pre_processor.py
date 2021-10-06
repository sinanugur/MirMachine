import hashlib
import json
from lookupService.serializers import JobSerializer
from lookupService.helpers.ncbi_fetcher import get_fasta


def process_form_data(request):
    serializer = JobSerializer(data=json.loads(request.POST.get('data')))
    if serializer.initial_data['mode'] == 'file':
        file = request.FILES.get('file')
        parsed_header = False
        _list = []
        for chunk in file.chunks():
            decoded = chunk.decode('utf-8')
            if not parsed_header:
                if serializer.initial_data['species'] == '':
                    lines = decoded.splitlines()
                    serializer.initial_data['species'], i = extract_fasta_header(lines)
                    _list.append(''.join(lines[i:]))
                parsed_header = True
                continue
            _list.append(decoded)
        serializer.initial_data['data'] = ''.join(_list)
    elif serializer.initial_data['mode'] == 'accNum':
        data = get_fasta(serializer.initial_data['data'])
        data = data.splitlines()
        i = 1
        if serializer.initial_data['species'] == '':
            serializer.initial_data['species'], i = extract_fasta_header(data)
        serializer.initial_data['data'] = ''.join(data[i:])
    serializer.initial_data['hash'] = hashlib.md5(serializer.initial_data['data'].encode()).hexdigest()
    return serializer


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

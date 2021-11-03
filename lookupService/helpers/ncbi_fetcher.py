import urllib3
from xml.dom import minidom
from MirMachineWebapp import user_config as config

baseURL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'


def get_fasta(accession_num):
    http = urllib3.PoolManager()
    response = http.request(
        'GET',
        baseURL + 'epost.fcgi?db=Nucleotide&id=' + accession_num
    )
    data = response.data.decode('utf-8')
    # print(data)
    xml = minidom.parseString(data)
    error = xml.getElementsByTagName('ERROR')
    if len(error) != 0:
        raise ValueError('Invalid accession number')
    query_key = xml.getElementsByTagName('QueryKey')[0].firstChild.data
    web_env = xml.getElementsByTagName('WebEnv')[0].firstChild.data
    response = http.request(
        'GET',
        baseURL + 'efetch.fcgi?db=Nucleotide&query_key=' + query_key +
        '&WebEnv=' + web_env + '&rettype=fasta&retmode=text'
    )
    if len(response) > config.MAX_NCBI_GENOME_SIZE:
        raise PermissionError('Genome exceeds the maximum size')
    decoded = response.data.decode('utf-8')
    if 'error' in decoded:
        raise RuntimeError
    print(decoded)
    return decoded


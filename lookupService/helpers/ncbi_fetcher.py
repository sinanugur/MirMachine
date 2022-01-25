import urllib3
import shutil
import json
import gzip
import os
import hashlib
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
    decoded = response.data.decode('utf-8')
    if len(decoded) > config.MAX_NCBI_GENOME_SIZE:
        raise PermissionError('Genome exceeds the maximum size')
    if 'error' in decoded:
        raise RuntimeError
    print(decoded)
    return decoded


def get_ftp_url(term):
    http = urllib3.PoolManager()
    response = http.request(
        'GET',
        baseURL + 'esearch.fcgi?db=assembly&retmode=json&term=' + term
    )
    parsed = json.loads(response.data.decode('utf-8'))
    result = parsed['esearchresult']
    if result['count'] == '0':
        return
    uid = result['idlist'][0]
    response = http.request(
        'GET',
        baseURL + 'esummary.fcgi?db=assembly&retmode=json&id=' + uid
    )
    parsed = json.loads(response.data.decode('utf-8'))
    result = parsed['result'][uid]
    ftp_directory = result['ftppath_genbank']
    split_path = ftp_directory.split('/')
    ftp_file = ftp_directory + '/' + split_path[len(split_path)-1] + '_genomic.fna.gz'
    return ftp_file


def fetch_from_ftp(term):
    ftp_url = get_ftp_url(term)
    if ftp_url is None:
        return ''
    http_url = 'http:' + ftp_url.split(':')[1]
    file_name = 'media/uploads/' + term + '.fa.gz'
    unzipped_name = file_name[:-3]
    http = urllib3.PoolManager()
    with http.request('GET', http_url, preload_content=False) as resp, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(resp, out_file)
    _hash = ''
    try:
        with gzip.open(file_name, 'rb') as zipped:
            with open(unzipped_name, 'wb') as unzipped:
                shutil.copyfileobj(zipped, unzipped)
                _hash = hashlib.md5(zipped.read()).hexdigest()
    except gzip.BadGzipFile:
        if os.path.exists(file_name):
            os.remove(file_name)
            os.remove(unzipped_name)
        return ''
    if os.path.exists(file_name):
        # Removing zipped file, don't need it
        os.remove(file_name)
    return unzipped_name, _hash





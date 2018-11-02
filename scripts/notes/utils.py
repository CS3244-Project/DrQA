from difflib import SequenceMatcher
import csv
import ntpath
import re
import requests
import subprocess
import uuid
import os

def run_cmd(cmd, verbose=True):
    if verbose:
        print(cmd)
    subprocess.call(['bash', '-c', cmd])

def normalize(s):
	s = s.lower()
	s = re.sub('\\(cid:.*?\\)', ' ', s)
	s = s.replace("'", " ").replace("-", " ").replace("`", " ").replace("(", " ").replace(")", " ")
	s = re.sub("\s\s+", " ", s)
	s = s[:-1] if (len(s) > 0 and s[-1] == ".") else s
	return s
    
def capture_regex(doc, mystr, squash=True):
    if squash:
        return mystr
    str2insert = "[\s(</newline>)(</tab>)\s]*"
    regex_pattern = ".*(" + str2insert + str2insert.join([re.escape(s) for s in mystr.split(' ')]) + str2insert + ").*"
    try:
        m = re.search(regex_pattern, doc)
    except Exception as e:
        print(doc)
        print(mystr)
        raise e
    return m.group(1) if m else mystr

def get_gdrive_id(url):
	m = re.search('https://drive.google.com/file/d/(.+?)/view\?usp=sharing', url)
	if m:
		return m.group(1)
	m = re.search('https://drive.google.com/open\?id\=(.+?)$', url)
	return m.group(1) if m else "default"

def is_similar_str(str1, str2, threshold=0.8):
	str1 = re.sub(r'\W+', '', str1)
	str2 = re.sub(r'\W+', '', str2)
	score = SequenceMatcher(None, str1, str2).ratio()
	return score >= threshold

def get_uuid(str_len=24):
	return str(uuid.uuid4())[:str_len]

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def write2csv(data, out_path, header=None):
	csv_file_out = open(out_path, 'wt')
	csv_writer = csv.writer(csv_file_out, delimiter=',', lineterminator='\n')
	if header:
		csv_writer.writerow(header)

	for d in data:
		csv_writer.writerow(d)

	csv_file_out.close()

def download_gdrive(id, destination):  
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def save_data(path, py_object):
    with open(path, 'wb') as f:
        pickle.dump(py_object, f)


# Load data from existing pickle
def load_data(pickle_in):
    with open(pickle_in, 'rb') as f:
        contents = pickle.load(f)
    return contents


def isfile(path):
    return os.path.isfile(path)


def time_format(second):
    h = second // 3600
    m = ((second % 3600) // 60)
    s = second % 60
    return [h, m, s]

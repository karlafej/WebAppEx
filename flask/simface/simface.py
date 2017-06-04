import cognitive_face as CF
from facekey import KEY
import csv

BASE_URL = 'https://westus.api.cognitive.microsoft.com/face/v1.0/' 
CF.BaseUrl.set(BASE_URL)
CF.Key.set(KEY)
imageset = {'science' : 4, 'movie' : 5, 'porn' : 2}
infos = dict()
idx = {  'porn' : "../../data/pornhub_list.tsv",
         'movie' : "../../data/imdb_list.tsv",
         'science' : "../../data/science_list.tsv"}

for setid, path in idx.items(): 
    info = []
    with open(path, 'r',  encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter = '\t')
        for row in reader:
            info.append(row)
        infos[setid] = info

def get_face_id(img_url):
	face_id = CF.face.detect(img_url, attributes='')[0]['faceId']
	return face_id


def face_similar(face_id, list_id):
    similars = CF.face.find_similars(face_id = face_id, face_list_id = list_id, mode = 'matchFace')
    return similars

def get_info(idx, face):
    results = dict()
    hit = [item for item in infos[idx] if item['faceId'] == face]        
    results['name'] = hit[0].get('name')
    results['url'] = hit[0].get('url')
    results['link'] = hit[0].get('link', '.')
    return results

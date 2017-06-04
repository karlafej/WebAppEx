from spyre import server
import cognitive_face as CF
from facekey import KEY
import csv

class WCApp(server.App):
    title = "Seek your face"

    inputs = [{
        "type":'text',
        "label": 'Photo URL',
        "key": 'imgurl',
        "action_id": 'html1'
    },

    {
        "type":'radiobuttons',
        "label": 'Find your lookalike among',
        "options" : [
            {"label": "Scientists", "value":"science"},
            {"label":"Actors and Actresses", "value":"movie", "checked":True},
            {"label": "Pornstars", "value":"porn"}
        ],
      "key": 'imageset',
      "action_id": 'html1'
    },]


    outputs = [{
        "type": "html",
        "id": "html1",
    }]

    def __init__(self):
        BASE_URL = 'https://westus.api.cognitive.microsoft.com/face/v1.0/' 
        CF.BaseUrl.set(BASE_URL)
        CF.Key.set(KEY)
        self.imageset = {'science' : 4, 'movie' : 5, 'porn' : 2}
        self.infos = dict()
        idx = {  'porn' : "../data/pornhub_list.tsv",
         'movie' : "../data/imdb_list.tsv",
         'science' : "../data/science_list.tsv"}

        for setid, path in idx.items(): 
            info = []
            with open(path, 'r',  encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile, delimiter = '\t')
                for row in reader:
                    info.append(row)
                    self.infos[setid] = info
        

    def html1(self, params):
        text = ''
        results = dict()
        imgurl = params['imgurl']
        imgset = params['imageset']
        list_id = self.imageset[imgset]
        if len(imgurl)>0 :
            face_id = CF.face.detect(imgurl, attributes='')[0]['faceId']
            similars = CF.face.find_similars(face_id = face_id, face_list_id = list_id, mode = 'matchFace')
            results = dict()
            hit = [item for item in self.infos[imgset] if item['faceId'] == similars[0]['persistedFaceId']]        
            results['name'] = hit[0].get('name')
            results['url'] = hit[0].get('url')
            results['link'] = hit[0].get('link', '.')
            results['confidence'] = similars[0]['confidence']
            text = '<a href = "'+results['link']+'"><img src="'+results['url']+ '" style = "max-width:400px"></a><h3>'+ \
                    results['name']+'</h3> Confidence: '+str(results['confidence'])
        return text
   

if __name__ == '__main__':
    app = WCApp()
    app.launch()

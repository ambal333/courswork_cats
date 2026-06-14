import requests
import json
from API_TOKEN import API_KEY
class GetCats:
    json_data=[]
    _url='https://cataas.com/'
    def __init__(self,text,api_key):
        self.text=text
        self.api_key=api_key
    def _build_url(self,api_method):
        return f'{self._url}{api_method}'
    def getcat(self):
        params={'json':'true'}
        response=requests.get(self._build_url('cat/says/'+self.text),params=params)
        response.raise_for_status()
        data = response.json()
        print('фото кота получено')
        return data.get('url')
    def _new_folder(self,group):
        url='https://cloud-api.yandex.net/v1/disk/resources'
        params={'path':group}
        headers = {'Authorization': f'OAuth {self.api_key}'}
        response= requests.put(url,params=params,headers=headers)
        data = response.json()
        print('папка создана')
        return data.get('href')

    def import_disc(self):
        cat_url=self.getcat()
        group='PY-254'
        self._new_folder(group)
        params={'url':cat_url,'path':f'{group}/cat_{self.text}.jpg' }
        headers={'Authorization': f'OAuth {self.api_key}'}
        url='https://cloud-api.yandex.net/v1/disk/resources/upload'
        response=requests.post(url,params=params,headers=headers)
        response.raise_for_status()
        data=response.json()
        self.json_data.append({'name': f'cat_{self.text}', 'text': self.text})
        self._json_file_append_info()
        return 'фото добавлены'

    def _json_file_append_info(self):
        with open('info_cats/backup_report.json','w',encoding='utf-8') as f:
            json.dump(self.json_data,f,ensure_ascii=False,indent=2)
        with open('info_cats/backup_report.json',encoding='utf-8') as f:
            data=json.load(f)
            print(data)


cat=GetCats('bay',API_KEY)
res=cat.import_disc()
# res=cat.getcat()
# res=cat._new_folder('PY-254')
print(res)
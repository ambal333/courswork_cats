import requests
import json
import os
# from API_TOKEN import API_KEY
class GetCats:
    json_data=[]
    _url_cats='https://cataas.com/'
    _yandex_url='https://cloud-api.yandex.net/v1/disk/'
    def __init__(self,text,api_key):
        self.text=text
        self.api_key=api_key
    def _build_url(self,api_method):
        return f'{self._url_cats}{api_method}'
    def getcat(self):
        params={'json':'true'}
        response=requests.get(self._build_url('cat/says/'+self.text),params=params)
        response.raise_for_status()
        data = response.json()
        print('фото кота получено')
        return data.get('url')
    def _new_folder(self,group):
        params={'path':group}
        headers = {'Authorization': f'OAuth {self.api_key}'}
        response= requests.put(f'{self._yandex_url}resources',params=params,headers=headers)
        data = response.json()
        print('папка создана')
        return data.get('href')

    def import_disc(self):
        cat_url=self.getcat()
        group='PY-254'
        self._new_folder(group)
        params={'url':cat_url,'path':f'{group}/cat_{self.text}.jpg' }
        headers={'Authorization': f'OAuth {self.api_key}'}
        response=requests.post(f'{self._yandex_url}resources/upload',params=params,headers=headers)
        response.raise_for_status()
        data=response.json()
        info_photo={'name': f'cat_{self.text}', 'text': self.text,'link':cat_url}
        self._load_existing_report()
        self._json_file_append_info(info_photo)
        return 'фото добавлены'
    def _load_existing_report(self):
        if os.path.exists('info_cats/backup_report.json'):
            with open('info_cats/backup_report.json',encoding='utf-8') as f:
                self.json_data=json.load(f)
        else:
            self.json_data = []

    def _json_file_append_info(self,new_info):
        self.json_data.append(new_info)
        os.makedirs('info_cats', exist_ok=True)
        with open('info_cats/backup_report.json','w',encoding='utf-8') as f:
            json.dump(self.json_data,f,ensure_ascii=False,indent=2)
            f.flush()
            json_str=json.dumps(self.json_data,ensure_ascii=False,indent=2)
            print(json_str)

cat=GetCats('hello',API_KEY)
res=cat.import_disc()
print(res)
import requests


class PetFinder:

    def __init__(self, api_key: str, api_sec: str):
        self.api_key = api_key
        self.api_sec = api_sec
        self.base_url = 'https://api.petfinder.com/v2'

        self.client = requests.session()

    def auth(self):
        data = {'grant_type': 'client_credentials',
                'client_id': self.api_key,
                'client_secret': self.api_sec}

        response = self.client.post(f'{self.base_url}/oauth2/token',
                                    data=data)

        if response.status_code == 200:
            token = response.json()['access_token']
            self.client.headers = {'Authorization': f'Bearer {token}'}
            
            return token
            
        print('Error authenticating.')
        
        return None

    def get_organizations(self, **kwargs):
        params = kwargs
        params['limit'] = 10

        response = self.client.get(f'{self.base_url}/organizations', params=params)

        if response.status_code == 200:
            return response.json()['organizations']

        print('Error: ', response.status_code, response.headers, response.text)
        
        return None
    
    def get_organization(self, organization_id: id):
        
        response = self.client.get(f'{self.base_url}/organizations/{organization_id}')

        if response.status_code == 200:
            return response.json()['organization']

        print('Error: ', response.status_code, response.headers, response.text)
        
        return None

    def get_animal_types(self):
        
        response = self.client.get(f'{self.base_url}/types')

        if response.status_code == 200:
            return response.json()['types']

        print('Error: ', response.status_code, response.headers, response.text)
        
        return None
    
    def get_animal_breeds(self, animal_type: str):
        
        response = self.client.get(f'{self.base_url}/types/{animal_type}/breeds')

        if response.status_code == 200:
            return response.json()['breeds']

        print('Error: ', response.status_code, response.headers, response.text)
        
        return None
    
    def get_animals(self, **kwargs):

        response = self.client.get(f'{self.base_url}/animals', params=kwargs)

        if response.status_code == 200:
            return response.json()['animals']

        print('Error: ', response.status_code, response.headers, response.text)
        
        return None
    
    def get_animal(self, animal_id: int):
        
        response = self.client.get(f'{self.base_url}/animals/{animal_id}')
        
        if response.status_code == 200:
            return response.json()['animal']

        print('Error: ', response.status_code, response.headers, response.text)
        
        return None

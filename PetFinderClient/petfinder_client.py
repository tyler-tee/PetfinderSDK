import requests


class PetFinderAPI:

    def __init__(self, api_key: str, api_sec: str):
        self.api_key = api_key
        self.api_sec = api_sec
        self.base_url = 'https://api.petfinder.com/v2'

        self.client = requests.session()
    
    ERROR_DICT = {
                    401: "Unauthorized request, please check your credentials.",
                    403: "Insufficient access to the requested resource.",
                    404: "Requested resource could not be found.",
                    500: "Unexpected error - If the problem persists, please contact support."
                                }

    def _make_request(self, method, resource, **kwargs):
        url = f'{self.base_url}/{resource}'
        response = self.client.request(method, url, **kwargs)
        
        # Check for a successful response
        if response.status_code == 200:
            return {'success': True, 'data': response.json()}
            
        error_details = {
            'success': False,
            'status_code': response.status_code,
            'reason': response.reason,
            'message': self.ERROR_DICT.get(response.status_code,
                                           "An error occurred with your request."),
            'details': response.text
        }

        return error_details
    
    def auth(self) -> dict:
        data = {'grant_type': 'client_credentials',
                'client_id': self.api_key,
                'client_secret': self.api_sec}

        response = self._make_request('POST', 'oauth2/token', json=data)

        if response['success']:
            token = response['data']['access_token']

            self.client.headers = {'Authorization': f'Bearer {token}'}

            return response
        else:
            print(f"Error: {response['data']}")
            return response

    def get_organizations(self, limit: int = 20, **kwargs) -> dict:
        params = kwargs
        params['limit'] = limit
        
        response = self._make_request('GET', 'organizations', params=params)
        
        if response['success']:
            total_pages = response['data']['pagination']['total_pages']
            current_page = response['data']['pagination']['current_page']

            while current_page != total_pages:
                current_page += 1
                params['page'] = current_page
                next_response = self._make_request('GET', 'organizations', params=params)

                response['data']['organizations'].extend(next_response['data']['organizations'])
                response['data']['pagination'] = next_response['data']['pagination']

        return response
    
    def get_organization(self, organization_id: id) -> dict:
        resource = f'/organizations/{organization_id}'
        response = self._make_request('GET', resource)

        return response

    def get_animal_types(self):
        response = self._make_request('GET', 'types')

        return response
    
    def get_animal_breeds(self, animal_type: str):
        resource = f'types/{animal_type}/breeds'
        response = self._make_request('GET', resource)

        return response
    
    def get_animals(self, **kwargs):
        params = kwargs

        response = self._make_request('GET', 'animals', params=kwargs)
        
        if response['success']:
            total_pages = response['data']['pagination']['total_pages']
            current_page = response['data']['pagination']['current_page']

            while current_page != total_pages:
                current_page += 1
                params['page'] = current_page
                next_response = self._make_request('GET', 'animals', params=params)

                response['data']['animals'].extend(next_response['data']['animals'])
                response['data']['pagination'] = next_response['data']['pagination']

        return response
    
    def get_animal(self, animal_id: int):

        resource = f'animals/{animal_id}'
        response = self._make_request('GET', resource)

        return response

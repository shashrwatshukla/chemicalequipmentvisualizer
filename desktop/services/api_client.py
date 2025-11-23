import requests

class APIClient:
    def __init__(self):
        from config import API_BASE_URL
        self.base_url = API_BASE_URL
        self.session = requests.Session()
        self.csrf_token = None
        self.token = None
    
    def _get_csrf(self):
        csrf = self.session.cookies.get('csrftoken')
        if csrf:
            self.csrf_token = csrf
            self.session.headers['X-CSRFToken'] = csrf
    
    def _set_auth_header(self):
        if self.token:
            self.session.headers['Authorization'] = f'Token {self.token}'
    
    def _handle_response(self, response):
        try:
            if response.status_code in [200, 201]:
                return True, response.json()
            else:
                try:
                    data = response.json()
                except:
                    data = {}
                error_msg = data.get('error', 'HTTP {}'.format(response.status_code))
                print(f"❌ API Error: {error_msg}")
                return False, error_msg
        except Exception as e:
            print(f"❌ Response parsing error: {str(e)}")
            return False, 'Response error: {}'.format(str(e))
    
    def login(self, username, password):
        try:
            print(f"Logging in as: {username}")
            print(f"API Base URL: {self.base_url}")
            
            # POST login request directly (no GET needed)
            print("Sending login POST...")
            r = self.session.post('{}/login/'.format(self.base_url), 
                                 json={'username': username, 'password': password})
            print(f"Login response status: {r.status_code}")
            print(f"Login response text: {r.text[:500]}")
            
            success, result = self._handle_response(r)
            if success:
                self.token = result.get('token')
                print(f"✅ Token obtained: {self.token[:20] if self.token else 'None'}...")
                self._set_auth_header()
                self._get_csrf()
            return success, result
        except Exception as e:
            print(f"❌ Login exception: {str(e)}")
            import traceback
            traceback.print_exc()
            return False, str(e)
    
    def register(self, username, email, password):
        try:
            r = self.session.post('{}/register/'.format(self.base_url),
                                 json={'username': username, 'email': email, 'password': password})
            return self._handle_response(r)
        except Exception as e:
            return False, str(e)
    
    def verify_email(self, username, code):
        try:
            r = self.session.post('{}/verify-email/'.format(self.base_url),
                                 json={'username': username, 'code': code})
            return self._handle_response(r)
        except Exception as e:
            return False, str(e)
    
    def upload_dataset(self, file_path):
        try:
            self._get_csrf()
            with open(file_path, 'rb') as f:
                files = {'file': f}
                headers = {'X-CSRFToken': self.csrf_token} if self.csrf_token else {}
                r = self.session.post('{}/upload/'.format(self.base_url), 
                                     files=files, headers=headers)
            return self._handle_response(r)
        except Exception as e:
            return False, str(e)
    
    def get_datasets(self):
        try:
            r = self.session.get('{}/datasets/'.format(self.base_url))
            return self._handle_response(r)
        except Exception as e:
            return False, str(e)
    
    def get_dataset_detail(self, dataset_id):
        try:
            r = self.session.get('{}/datasets/{}/'.format(self.base_url, dataset_id))
            return self._handle_response(r)
        except Exception as e:
            return False, str(e)
    
    def get_dataset_summary(self, dataset_id):
        try:
            r = self.session.get('{}/datasets/{}/summary/'.format(self.base_url, dataset_id))
            return self._handle_response(r)
        except Exception as e:
            return False, str(e)
    
    def download_report(self, dataset_id, save_path):
        try:
            r = self.session.get('{}/datasets/{}/report/'.format(self.base_url, dataset_id), stream=True)
            if r.status_code == 200:
                with open(save_path, 'wb') as f:
                    for chunk in r.iter_content(8192):
                        f.write(chunk)
                return True, 'Success'
            return False, 'Failed'
        except Exception as e:
            return False, str(e)
    
    def delete_dataset(self, dataset_id):
        try:
            self._get_csrf()
            r = self.session.delete('{}/datasets/{}/delete/'.format(self.base_url, dataset_id))
            return self._handle_response(r)
        except Exception as e:
            return False, str(e)
    
    def logout(self):
        try:
            r = self.session.post('{}/logout/'.format(self.base_url))
            return self._handle_response(r)
        except Exception as e:
            return False, str(e)
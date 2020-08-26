'''
Author: aaronlyy (Aaron Levi)
Version: 0.1

This is a very simple and basic API Wrapper for the Spotify Web API.
'''

import requests # pip install requests


class Punktify():
    '''
    Create a new connection to the Spotify Web API using your client_id, client_secret and redirect_url.
    (Can be found on your Developer Dashboard.)
    '''
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

        # create a access_token variable with type None to check if a authorization has been made or not
        self.access_token = None


    def build_authorization_url(self, redirect_uri, scopes=[]):
        '''
        This function takes a list of scopes and returns a authorization URL with the given scopes.

            scopes: ugc-image-upload
                    user-read-playback-state
                    user-modify-playback-state
                    user-read-currently-playing
                    streaming
                    app-remote-control
                    user-read-email
                    user-read-private
                    playlist-read-collaborative
                    playlist-modify-public
                    playlist-read-private
                    playlist-modify-private
                    user-library-modify
                    user-library-read
                    user-top-read
                    user-read-playback-position
                    user-read-recently-played
                    user-follow-read
                    user-follow-modify
        '''
        scope = "%20".join(scopes) # add scopes together (urlencode?)
        url = "https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}".format(
            client_id=self.client_id, redirect_uri=redirect_uri, scope=scope)
        return url

    def request_access_token(self, authorization_code, redirect_uri, refresh=False):
        '''
        This function taken a authorization_code and requests an access token from it.
        if refresh is set to True, it requests an new access token using the refresh token.
        '''
        if refresh:
            grant_type = "refresh_token"
        else:
            grant_type = "authorization_code"

        data = {
            "grant_type": grant_type,
            "code": authorization_code,
            "redirect_uri": redirect_uri,
            "client_secret": self.client_secret,
            "client_id": self.client_id
        }
        url = "https://accounts.spotify.com/api/token"

        response = requests.post(url, data=data)

        return TokenResponse(response)


class TokenResponse():
    '''
    This class holds all the access information
    '''
    def __init__(self, response):
        self.jsonobj = response.json()
    
    def __getattr__(self, attr):
        '''
        get single attributes from the object
        '''
        if attr in self.jsonobj:
            return self.jsonobj[attr]
        else:
            return None
    
    def iter(self):
        '''
        returns a dict like object that can be iterated (key, value) (.items(), .keys(), .values())
        '''
        return self.jsonobj
            




if __name__ == "__main__":
    # create a connection
    pf = Punktify("8583112c962541aba4adb81", "cfca632aeaee4ed59b27")
    # build a authorization url with given scopes
    print(pf.build_authorization_url("https://8bdbb8ef4d82.ngrok.io", ["user-follow-modify"]))
    # request an access_token
    code = input("\nauth code: ")
    tokenres = pf.request_access_token(code, "https://8bdbb8ef4d82.ngrok.io")
    if tokenres.status_code == 200:
        print(tokenres.access_token)
    else:
        for k, v in tokenres.iter().items():
            print(k, v)
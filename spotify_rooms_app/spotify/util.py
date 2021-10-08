# Utility file

from rest_framework.response import Response
from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET
from requests import post, put, get

BASE_URL = "https://api.spotify.com/v1/me/"

def getUserTokens(session_key):
    user_tokens = SpotifyToken.objects.filter(user=session_key)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None
    
def updateOrCreateUserTokens(session_key, access_token, token_type, expires_in, refresh_token):
    tokens = getUserTokens(session_key)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=["access_token", "refresh_token", "expires_in", "token_type"])
    else:
        tokens = SpotifyToken(user=session_key, access_token=access_token, refresh_token=refresh_token, expires_in=expires_in, token_type=token_type)
        tokens.save()

def isAuthenticated(session_key):
    tokens = getUserTokens(session_key)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refreshToken(session_key)
        return True
    return False

def refreshToken(session_key):
    refresh_token = getUserTokens(session_key).refresh_token

    response = post("https://accounts.spotify.com/api/token", data={
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }).json()

    access_token = response.get("access_token")
    refresh_token = response.get("refresh_token")
    expires_in = response.get("expires_in")
    token_type = response.get("token_type")

    updateOrCreateUserTokens(session_key, access_token=access_token, token_type=token_type, expires_in=expires_in, refresh_token=refresh_token)

def executeSpotifyApiRequest(session_key, endpoint, post_=False, put_=False):
    tokens = getUserTokens(session_key)
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + tokens.access_token}

    if post_:
        post(BASE_URL + endpoint, headers=headers)
    if put_:
        put(BASE_URL + endpoint, headers=headers)

    response = get(BASE_URL + endpoint, {}, headers=headers)
    try:
        return response.json()
    except:
        return {'Error': 'Issue with request'}


import os


class Config(object):
    LOAD = []
    NO_LOAD = ['translation']
    API_KEY = "<bot-token>"
    OWNER_ID = "<user-id>"

    # Youtube credentials
    YOUTUBE_API_KEY = "<youtube-api-key>"

    # Spotify credentials
    os.environ["SPOTIPY_CLIENT_ID"] = "<spotify-api-client-id>"
    os.environ["SPOTIPY_CLIENT_SECRET"] = "<spotify-api-secret-key>"
    os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost:8000/callback/'
    username = "<spotify-username>"
    scope = 'user-read-private'

    # webhoooks
    priv_key = '<location-of-private-key>'
    cert_pem = '<location-of-cert.pem>'
    webhook_url = 'https://<url>:<port>/'

    # Boolean switch for webhooks
    use_webhooks = False

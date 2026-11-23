from authlib.integrations.flask_oauth2 import AuthorizationServer
from authlib.oauth2.rfc7636 import CodeChallenge

from app.extensions import db
from app.models.oauth import OAuth2Client, OAuth2Token
from app.services.oauth_grants import AuthorizationCodeGrant


authorization_server = AuthorizationServer()


def query_client(client_id):
    return OAuth2Client.query.filter_by(client_id=client_id).first()


def save_token(token, request):
    if not request.user:
        raise RuntimeError("OAuth token cannot be saved without an authenticated user.")

    token_data = dict(token)
    token_data["client_id"] = request.client.client_id
    token_data["user_id"] = request.user.id

    oauth_token = OAuth2Token(**token_data)
    db.session.add(oauth_token)
    db.session.commit()


def init_oauth_server(app):
    authorization_server.init_app(
        app,
        query_client=query_client,
        save_token=save_token,
    )

    authorization_server.register_grant(
        AuthorizationCodeGrant,
        extensions=[
            CodeChallenge(required=True),
        ],
    )

    return authorization_server

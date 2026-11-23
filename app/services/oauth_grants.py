from authlib.oauth2.rfc6749 import grants
from app.extensions import db
from app.models.oauth import OAuth2AuthorizationCode
from app.models.user import User


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):

    def save_authorization_code(self, code, request):
        client = request.client

        authorization_code = OAuth2AuthorizationCode(
            code=code,
            client_id=client.client_id,
            redirect_uri=request.redirect_uri,
            response_type=request.payload.response_type,
            scope=request.scope,
            user_id=request.user.id,
            nonce=request.payload.data.get("nonce"),
            code_challenge=request.payload.data.get("code_challenge"),
            code_challenge_method=request.payload.data.get(
                "code_challenge_method"
            ),
        )

        db.session.add(authorization_code)
        db.session.commit()
        return authorization_code

    def query_authorization_code(self, code, client):
        authorization_code = OAuth2AuthorizationCode.query.filter_by(
            code=code,
            client_id=client.client_id,
        ).first()

        if authorization_code and not authorization_code.is_expired():
            return authorization_code

        return None

    def delete_authorization_code(self, authorization_code):
        db.session.delete(authorization_code)
        db.session.commit()

    def authenticate_user(self, authorization_code):
        return db.session.get(User, authorization_code.user_id)

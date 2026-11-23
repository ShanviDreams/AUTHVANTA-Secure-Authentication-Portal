from app.extensions import db
from authlib.integrations.sqla_oauth2 import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OAuth2TokenMixin,
)


class OAuth2Client(db.Model, OAuth2ClientMixin):
    __tablename__ = "oauth2_clients"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(48), unique=True, nullable=False, index=True)


class OAuth2AuthorizationCode(db.Model, OAuth2AuthorizationCodeMixin):
    __tablename__ = "oauth2_authorization_codes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    user = db.relationship("User")

    def get_user(self):
        return self.user


class OAuth2Token(db.Model, OAuth2TokenMixin):
    __tablename__ = "oauth2_tokens"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    user = db.relationship("User")

    def get_user(self):
        return self.user

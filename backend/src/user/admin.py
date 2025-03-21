from sqladmin import ModelView

from user.models import User, OAuthAccount


class UserAdmin(ModelView, model=User):
    name='User'
    name_plural='Users'
    column_list = [
        "id",
        "username",
        "email",
        "hashed_password",
        "registered_at",
        "telegram",
        "whatsapp",
        "linkedin",
        "phone_number",
        "subscription_type"
        "profile_picture_url",
        "is_active",
        "is_superuser",
        "is_verified",
    ]

    form_create_rules = [
        "username", 
        "email", 
        "password", 
        "telegram", 
        "whatsapp", 
        "linkedin", 
        "phone_number", 
        "profile_picture_url", 
        "subscription_type",
        "is_active", 
        "is_superuser", 
        "is_verified"
    ]

    form_widget_args = {
        'hashed_password': {
            'type': 'password'
        }
    }

    column_labels = {
        "id": "ID",
        "username": "Username",
        "email": "Email",
        "hashed_password": "Password",
        "registered_at": "Registered At",
        "telegram": "Telegram",
        "whatsapp": "Whatsapp",
        "linkedin": "LinkedIn",
        "subscription_type": "Subscription Type",
        "phone_number": "Phone Number",
        "profile_picture_url": "Profile Picture",
        "is_active": "Active",
        "is_superuser": "Superuser",
        "is_verified": "Verified",
    }

    form_choices = {
        'is_active': [
            (True, 'Active'),
            (False, 'Inactive')
        ],
        'is_superuser': [
            (True, 'Yes'),
            (False, 'No')
        ],
        'is_verified': [
            (True, 'Yes'),
            (False, 'No')
        ],
        "subscription_type": [
            ("free", "Free"),
            ("premium", "Premium")
        ]
    }



class OAuthAccountAdmin(ModelView, model=OAuthAccount):
    name='OAuth Account'
    name_plural='OAuth Accounts'
    column_list = [
        "id",
        "user_id",
        "oauth_name",
        "access_token",
        "expires_at",
        "refresh_token",
        "account_id",
        "account_email",
    ]
    form_create_rules = [
        "oauth_name", 
        "access_token", 
        "expires_at", 
        "refresh_token", 
        "account_id", 
        "account_email",
    ]
    form_widget_args = {
        'expires_at': {
            'type': 'datetime-local'
        }
    }
    column_labels = {
        "id": "ID",
        "user_id": "User ID",
        "oauth_name": "OAuth Name",
        "access_token": "Access Token",
        "expires_at": "Expires At",
        "refresh_token": "Refresh Token",
        "account_id": "Account ID",
        "account_email": "Account Email",
    }
## social_media_api - Accounts

Endpoints:
- POST /api/accounts/register/  -> register and returns token
- POST /api/accounts/login/     -> login (username+password) returns token + user
- GET/PATCH /api/accounts/profile/ -> get/update own profile (token required)

Auth:
- Token authentication (Authorization: Token <token>)
- DRF session auth also enabled for browsable API.

Custom user:
- fields: username, email, bio, profile_picture, followers (M2M)

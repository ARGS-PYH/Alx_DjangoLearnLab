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

# Posts API

Endpoints:
- GET /api/posts/               -> list posts (supports search, filter, ordering, pagination)
- POST /api/posts/              -> create post (auth required)
- GET /api/posts/{id}/          -> retrieve post (includes nested comments)
- PUT/PATCH /api/posts/{id}/    -> update post (owner only)
- DELETE /api/posts/{id}/       -> delete post (owner only)

Comments:
- GET /api/comments/
- POST /api/comments/           -> create comment (auth required)
- PUT/PATCH /api/comments/{id}/ -> update comment (owner only)
- DELETE /api/comments/{id}/    -> delete comment (owner only)

Filtering:
- use ?search=keyword, ?ordering=created_at, ?page=2, ?author__username=username

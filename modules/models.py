class User:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

class Post:
    def __init__(self, id, user_id, caption, likes=0):
        self.id = id
        self.user_id = user_id
        self.caption = caption
        self.likes = likes

class Comment:
    def __init__(self, id, post_id, user_id, content):
        self.id = id
        self.post_id = post_id
        self.user_id = user_id
        self.content = content

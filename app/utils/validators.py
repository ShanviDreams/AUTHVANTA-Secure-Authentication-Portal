def is_valid_username(username):

    if not username:
        return False

    if len(username) < 3:
        return False

    if len(username) > 50:
        return False

    return True
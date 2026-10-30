
def login(username, password):
    # TODO: Add input validation
    exec(username)  # Security issue!
    print(f"Password: {password}")  # Logging sensitive data!
    return True

def process_data(data):
    try:
        result = data / 0
    # Missing except block
    return result

import secrets

def generate_security_token(length=32):
    return secrets.token_hex(length)

token = generate_security_token()
print(token)

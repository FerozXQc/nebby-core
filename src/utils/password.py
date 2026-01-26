import bcrypt
salt = bcrypt.gensalt()
def generate_hashed_password(plain_password:str):
    byte_password = plain_password.encode('utf-8')
    return bcrypt.hashpw(byte_password,salt).decode('utf-8')

def verify_hashed_password(plain_password:str,hashed_password:str):
    byte_password,hashed_password = plain_password.encode('utf-8') , hashed_password.encode('utf-8')
    return bcrypt.checkpw(byte_password,hashed_password)
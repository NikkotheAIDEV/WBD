import bcrypt

# Encode the password
password = "TestPassword"
password = password.encode('utf-8')

# Generate the salt and hash
salt = bcrypt.gensalt(rounds=14)
hashed = bcrypt.hashpw(password, salt)

# Check for a match
if bcrypt.checkpw(password, hashed):
    print("match")
password = 'password1'
for i in list(range(0,10)):
    if str(i) not in password:
        password_split = password.split(str(i))
        print(password)

text = password.split()
print(text)
# 加密器
def supply_reset():
    global supply
    with open('supply.txt',"r") as f :
        one = f.readline()[:-1]
        two = f.readline()[:-1]
        three = f.readline()
        supply = list(one+two+two.upper()+three)

def flush(a,b):
    global supply
    a, b = int(a), int(b)
    if a>b:
        a, b = b, a
    b = b*(3)
    add = supply[a:b]
    del supply[a:b]
    for k in range(len(add)):
        supply.append(add[k])

def encode(master_key:int, password:int):
    if master_key == 1 : return
    global supply 
    supply_reset()
    mul = 0    
    rest = 0
    rest_master_key = master_key
    while len(str(master_key)) < len(str(password))*2:
        mul += 1
        master_key = rest_master_key**mul
    master_key = list(str(master_key))
    encoded = str(len(str(mul)))+str(mul)
    for i in password :                
        flush(master_key[rest],master_key[rest+1])
        rest += 2
        rest_encode = str(supply.index(i))
        encoded += str(len(rest_encode))+rest_encode
    return encoded

def decode(master_key:int, encoded:str):
    global supply
    supply_reset()
    password = ''
    count, master_count = 0, 0
    mul_number = int(encoded[count])
    count = mul_number
    master_mul = int(''.join(encoded[1:mul_number+1]))
    master_key = list(str(int(master_key)**master_mul))          
    while count+1 < len(encoded):
        count += 1
        flush(master_key[master_count],master_key[master_count+1])
        master_count += 2 
        number_len = int(encoded[count])
        rest_password = int(''.join(encoded[count+1:count+number_len+1]))
        count += number_len
        password += supply[rest_password]
    return password


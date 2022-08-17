import random
import string

class PasswordSettings():
    
    def __init__(self,pw_length = 8,special_words = False):
        self.pw_length = pw_length
        self.special_words = special_words     

    def genPw(self):
            password_li = []
            
            count = 0
            while count < self.pw_length:
                rndm_letter = random.choice(string.ascii_letters)
                rndm_num = random.randint(0,9)
                rndm_index = random.randint(0,1)
                possible = [rndm_letter,rndm_num]
                
                password_li.append(possible[rndm_index])
                count += 1
                
            password = ''.join(str(x) for x in password_li)
            password = self.spclPassword(self.special_words,password)
            
            print(password)
            return password
        
    def spclPassword(self,word,pswrd):
        rndm_num = random.randint(0,9)
        pswrd_li = list(pswrd.strip())
        if word != '':
            if "," in word:
                word_li = word.split(",")
                for element in word_li :
                    pswrd_li.append(self.rndmUpLowerCase(element))
                random.shuffle(pswrd_li)
                new_pswrd = ''.join(pswrd_li)
                return new_pswrd  
            else:
                return pswrd[:rndm_num] + self.rndmUpLowerCase(word) + pswrd[rndm_num:]
        else:
            return pswrd
            
    def rndmUpLowerCase(self,input):
        new_str = ''
        if isinstance(input,str):
            for char in input:
                rnd_num = random.randint(0,1)
                up_low = [char.upper(),char.lower()]
    
                new_str += up_low[rnd_num]  
            return new_str    
        else:    
            for element in input:
                for char in element:
                    rnd_num = random.randint(0,1)
                    up_low = [char.upper(),char.lower()]
        
                    new_str += up_low[rnd_num]
            return new_str 
        
    def process(self):
        pw = self.genPw()
        return pw    
    
        
def save(input):
    f = file("pw_save.txt")
    
    try:
        f.file.write(str(input))
    except:
        print("ERROR: COULD NOT SAVE PASSWORD")    
    return

class file():
    
    def __init__(self,filename, mode = "a+"):
        self.filename = filename
        self.mode = mode
        self.file = open(self.filename,self.mode)

        
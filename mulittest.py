import os

def run_all():
    os.system("python3 heat.py 0 2 250")
    os.system("python3 heat.py 0 6 250")  
    os.system("python3 heat.py 0 4 250")  
    os.system("python3 heat.py 1 2 250")  
    os.system("python3 heat.py 1 4 250")
    os.system("python3 heat.py 1 6 250")
    os.system("python3 heat.py 0 2 500")
    os.system("python3 heat.py 0 6 500")  
    os.system("python3 heat.py 0 4 500")    

run_all()

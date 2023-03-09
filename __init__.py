from datetime import datetime
a = '17/03/2023'

#x_new = datetime.strptime(a,  "%Y-%m-%d %H:%M:%S").date()
teste = datetime.strptime(a, '%d/%m/%Y')
print(teste)
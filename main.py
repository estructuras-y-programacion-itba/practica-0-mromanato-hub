import random 

def tirada(cant_dados): 
    #dado1 = random.randint(1,6)
    #dado2 = random.randint(1,6)
    #dado3 = random.randint(1,6)
    #dado4 = random.randint(1,6)
    #dado5 = random.randint(1,6)
    #return dado1,dado2,dado3,dado4,dado5

    #mejora con ciclo for
    tirada = []
    for i in range(cant_dados):
         tirada.append(random.randint(1,6))

    return tirada
      
def evaluar_tirada(tirada):
    pass







def main():
    print('Cuantos dados tiras?')
    cant_dados = int(input())
    tirada1 = tirada(cant_dados=cant_dados)
    print('tirada 1:')
    print(tirada1)
    print('que posiciones te quedas? escribi el numero de la posicion separada con ,')
    posiciones = input()


# No cambiar a partir de aqui
if __name__ == "__main__":
    main()
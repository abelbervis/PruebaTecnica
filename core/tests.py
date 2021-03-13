
class ListaEnlazada(object):

    def __init__(self):
        self.__primero = None
        self.__ultimo = None
        self.__leng = 0

    class Elemento(object):
        def __init__(self, elemento):
            # atributos del nodo
            self.__elemento = elemento
            # puntero de union
            self.__pSig = None

        def get_elemento(self):
            return self.__elemento

        def __str__(self):
            return self.__elemento.__str__()

        def get_id(self):
            return self.__elemento.get_id()


    def estaVacia(self):
        if self.__primero == None:
            return True

    def insertarAlInicio(self,elemento):
        nuevo = self.Elemento(elemento)
        # si esta vacio se apuntara a el unico elemento
        if self.estaVacia():
            self.__primero = self.__ultimo = nuevo
        else:
        # si la lista tiene datos el siguiente de nuevo apuntara al primero
            nuevo.pSig = self.__primero
        # el primero de la lista sera el nuevo
            self.__primero = nuevo
        self.__leng += 1

    def insertarDespuesActual(self,actual,elemento):
        nuevo = self.Elemento(elemento)
        # si esta vacio se apuntara a el unico elemento
        if self.estaVacia():
            self.__primero = self.__ultimo = nuevo
        else:
            if actual == self.__ultimo:

                actual.pSig = elemento
                self.__ultimo = elemento
            else:
                temp = actual.pSig
                actual.pSig = elemento
                elemento.pSig = temp
                temp = None
        self.__leng += 1

    def cambiarElementoActual(self, id):

        if self.estaVacia():
            print("lista vacia")
        else:
            validar = True
            temp = self.__primero
            while (validar):
                if str(temp.get_id()) == id:
                    return temp
                else:
                    temp = temp.pSig


    def iterarLista(self):
        validar = 's'
        temp = self.__primero
        while(validar == 's'):
            if self.estaVacia():
                return "Lista vacia"
            else:
                print('******************** Menu ********************')
                print('-------------- Detalle de lista --------------')
                print('|longitud='+str(self.__leng)+'|ultimoNodo('+str(self.__ultimo)+')|')
                print('----------------------------------------------')
                print('-------------- ELEMENTO ACTUAL: --------------')
                print(temp.get_elemento())
                print('----------------------------------------------')
                print('escoja la opcion que desee realizar: ')
                print('1- Eliminar el elemento actual')
                print('2- Avanzar al siguiente nodo de la lista')
                print('3- Imprimir lista')
                print('4- Agregar nuevo registro')
                print('5- Cambiar el elemento actual')
                if(self.estaVacia() != True):
                    print('6- Insertar tras el elemento actual ')
                print('**********************************************')
                respuesta = input('Opcion=')

                if respuesta == '1':
                    print("Esta seguro de eliminar el siguiente registro? 1- si, 2- no. ")
                    re = input("R= ")
                    if re == '1':
                        self.eliminar2(temp)
                        temp = self.__primero
                    elif re == '2':
                        pass
                    else:
                        print('ingrese una opcion valida')
                elif respuesta == '2':
                    if temp != self.__ultimo:
                        temp = temp.pSig
                    else:
                        temp = self.__primero
                elif respuesta == '3':
                    self.imprimirLista()
                elif respuesta == '4':
                    print('Ingrese el nombre del cliente:')
                    self.insertarAlInicio(self.Elemento(Cliente(str(self.__leng+1),input('R='))))
                elif respuesta == '5':

                    v=True
                    while v==True:
                        print('Ingrese el id del registro del 1 al '+str(self.__leng))
                        i = input('R=')
                        try:
                            if 0 < int(i) and int(i) < self.__leng + 1:
                                temp = self.cambiarElementoActual(i);
                                v = False
                        except Exception as  e:
                            print(e)



                elif respuesta == '6' and not self.estaVacia():
                    print('Ingrese el nombre del cliente:')
                    self.insertarDespuesActual(temp,self.Elemento(Cliente(str(self.__leng+1),input('R='))))
                else:
                    print('Alerta!: Ingrese una opcion valida')


    def eliminar2(self, elemento):
        # si la lista esta vacia
        if self.estaVacia():
            print("No se puede eliminar,lista vacia")
        # si solo hay un elemento
        elif self.__primero == self.__ultimo:
            self.__primero = None
            self.__ultimo = None
            print('Elemento eliminado con exito, lista vacia!')
            self.__leng-=1

        # si hay mas de un elemento
        else:
            validar = True
            temp = self.__primero
            while(validar):
                print('-----------temp.pSig')
                print(temp.pSig)
                print('-----------self.__ultimo')
                print(self.__ultimo)

                if temp == self.__ultimo:
                    print('eliminando el ultimo nodo')
                    temp2 = self.__ultimo
                    self.__ultimo = temp
                    temp2 = None
                    self.__leng-=1
                    print('Elemento eliminado!')
                    validar = False
                    print('---------Temporal se supone que es el primero!')
                    print(temp)
                if elemento == temp:
                    print('eliminando cualquiera menos el ultimo')
                    temp2 = temp
                    self.__primero = temp2.pSig
                    temp2 = None
                    validar = False
                    self.__leng -= 1
                    print('1er Elemento eliminado!')
                    self.imprimirLista()
                    temp = temp.pSig
                else:
                    temp = temp.pSig




    def imprimirLista(self):
        if self.estaVacia():
            return "Lista vacia!"
        else:
            validar = True
            temp = self.__primero
            print('|------------------- Listar elementos -----------------------|')
            while(validar == True):
                print(' -'+str(temp.get_elemento()))
                if temp == self.__ultimo:
                    validar = False
                else:
                    temp = temp.pSig
            print('|------------------------------------------------------------|')


    def getPrimero(self):
        if self.estaVacia():
            return "Lista vacia"
        else:
            return self.__primero

    def getUltimo(self):
        if self.estaVacia():
            return "Lista vacia"
        else:
            return self.__ultimo

    def getLeng(self):
        return self.__leng

class Cliente(object):

    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

    def __str__(self):
        return 'cliente:  id="'+str(self.id) +'" nombre="'+ self.nombre+'"'

    def get_id(self):
        return self.id


l = ListaEnlazada()

cl1 = Cliente(1,"Abel Bervis")
cl2 = Cliente(2, "Telma Ramos")
cl3 = Cliente(3, "Karla Quintero")
if l.estaVacia():
    l.insertarAlInicio(l.Elemento(cl1))
    l.insertarAlInicio(l.Elemento(cl2))
    l.insertarAlInicio(l.Elemento(cl3))
    l.iterarLista()
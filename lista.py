"""
Esse código tem a intenção de implementar listas em python! (As de verdade)
"""

class Elemento:
    """
    A classe elemento, a mais básica de todas. Armazena um Elemento associado à um identificador único
    (é responsabilidade do usuário garantir a unicidade do elemento/identificador)

    """
    def __init__(self, elemento):
        self.__elemento: Elemento = elemento
        self.__prox: Elemento = None
        self.__ant: Elemento = None

    @property
    def elemento(self):
        return self.__elemento

    @property
    def prox(self):
        return self.__prox

    @prox.setter
    def prox(self, prox):
        self.__prox = prox

    @property
    def ant(self):
        return self.__ant

    @ant.setter
    def ant(self, ant):
        self.__ant = ant

class Lista:
    """
    A classe lista conta com 3 ponteiros principais: `inicio`, `fim` e o `cursor`.
    Além disso, tabém conta com o atributo `tamanho` para facilitar operações
    """
    def __init__(self):
        self.__inicio : Elemento = None
        self.__fim : Elemento = None
        self.__cursor : Elemento = None
        self.__tamanho: int = 0

    def __avançarKPosições(self, k):
        """
        Considerando a posição atual do `cursor`, avança `k` posições
        """
        for _ in range(k):
            if self.__cursor:
                self.__cursor = self.__cursor.prox
            else:
                return

    def __retrocederKPosições(self, k):
        """
        Considerando a posição atual do `cursor`, retrocede `k` posições
        """
        for _ in range(k):
            if self.__cursor:
                self.__cursor = self.__cursor.ant
            else:
                return

    def __irParaPrimeiro(self):
        """
        Faz o `cursor` apontar para o `inicio`
        """
        self.__cursor = self.__inicio

    def __irParaUltimo(self):
        """
        Faz o `cursor` apontar para o `fim`
        """
        self.__cursor = self.__fim

    def acessarAtual(self):
        """
        Retorna o valor do elemento para o qual o `cursor` aponta. Caso esteja aterrado, retorna None.
        """
        if self.__cursor:
            return self.__cursor.elemento
        return None

    def InserirAntesDoAtual(self, novo: int) -> None:
        """
        Insere um `novo` elemento na lista antes do elemento apontado pelo `cursor`, que é redirecionado para esse novo elemento.
        O cursor não pode estar aterrado para essa operação (Lista Vazia).
        """
        if self.__cursor is None:
            return
        elif self.__cursor == self.__inicio:
            self.inserirComoPrimeiro(novo)
            return

        novo_elemento = Elemento(novo)
        ANTES = self.__cursor.ant

        novo_elemento.prox = self.__cursor
        novo_elemento.ant = ANTES

        ANTES.prox = novo_elemento
        self.__cursor.ant = novo_elemento

        self.__tamanho += 1
        self.__retrocederKPosições(1)   


    def InserirApósAtual(self, novo: int) -> None:
        """
        Insere um `novo` elemento na lista após o elemento apontado pelo `cursor`, que é redirecionado para esse novo elemento.
        O cursor não pode estar aterrado para essa operação (Lista Vazia).
        """
        if self.__cursor is None:
            return
        
        if self.__cursor == self.__fim:
            self.inserirComoUltimo(novo)
            return

        novo_elemento = Elemento(novo)
        DEPOIS = self.__cursor.prox

        novo_elemento.ant = self.__cursor
        novo_elemento.prox = DEPOIS

        self.__cursor.prox = novo_elemento
        DEPOIS.ant= novo_elemento

        self.__tamanho += 1
        self.__avançarKPosições(1)

    def inserirComoUltimo(self, novo: int) -> None:
        """
        Insere um `novo` elemento no fim da lista. O `cursor` é redirecionado para esse novo elemento.
        """
        if self.__inicio is None:
            self.inserirComoPrimeiro(novo)
            return
        novo_elemento = Elemento(novo)

        novo_elemento.ant = self.__fim
        self.__fim.prox = novo_elemento
        self.__fim = novo_elemento

        self.__irParaUltimo()
        self.__tamanho += 1

    def inserirComoPrimeiro(self, novo: int) -> None:
        """
        Insere um `novo` elemento no inicio da lista. O `cursor` é redirecionado para esse novo elemento.
        """
        novo_elemento = Elemento(novo)

        if self.__inicio is None:
            self.__inicio = novo_elemento
            self.__fim = novo_elemento
            self.__cursor = novo_elemento
        else:
            novo_elemento.prox = self.__inicio
            self.__inicio.ant = novo_elemento
            self.__inicio = novo_elemento
        
        self.__irParaPrimeiro()
        self.__tamanho += 1


    def inserirNaPosicao (self, k: int, novo:int) -> None:
        """
        Caso a posição seja válida (0 <= k <= tamanho da lista),
        insere um `novo` elemento no na posição `k` e redireciona o cursor para esse elemento.
        """
        if k == 0:
            self.inserirComoPrimeiro(novo)
            return
        elif k == self.__tamanho:
            self.inserirComoUltimo(novo)
            return
        elif k > self.__tamanho - 1 or k < 0:
            return

        if (k >= self.__tamanho / 2):
            self.__irParaUltimo()
            self.__retrocederKPosições((self.__tamanho - 1) - k)
        else:
            self.__irParaPrimeiro()
            self.__avançarKPosições(k)

        self.InserirAntesDoAtual(novo)


    def ExcluirPrim(self) -> None:
        """
        Exclui o primeiro elemento da lista. Caso ela fique vazia, todos os ponteiros,
        inclusive o `cursor`, são aterrados. Caso contrário, o `cursor` vai para o novo primeiro
        elemento da lista.
        """
        if self.__inicio is None:
            return None

        if self.__tamanho == 1:
            self.__cursor = None
            self.__inicio = None
            self.__fim = None
        else:
            self.__inicio.prox.ant = None
            self.__inicio = self.__inicio.prox

        self.__irParaPrimeiro()
        self.__tamanho -= 1

    def ExcluirUlt(self) -> None:
        """
        Exclui o último elemento da lista. Caso a lista seja unitária, chama o método `ExcluirPrim`.
        O `cursor` é redirecionado para o novo último elemento
        """
        if self.__inicio is None:
            return None
        if self.__tamanho == 1:
            self.ExcluirPrim()
            return
        self.__fim = self.__fim.ant
        self.__fim.prox = None

        self.__irParaUltimo()
        self.__tamanho -= 1

    def ExcluirAtual(self) -> None:
        """
        Exclui o elemento apontado pelo `cursor`. Caso a lista seja unitária, chama o método `ExcluirPrim`.
        Ao fim, o `cursor` apontará para o anterior do excluido. Caso o cursor esteja aterrado, retorna None.
        """
        if (self.__inicio is None) or (self.__cursor is None):
            return None
        elif self.__cursor == self.__inicio:
            self.ExcluirPrim()
            return None
        elif self.__cursor == self.__fim:
            self.ExcluirUlt()
            return None
        
        ANTES = self.__cursor.ant
        DEPOIS = self.__cursor.prox

        ANTES.prox = DEPOIS
        DEPOIS.ant = ANTES

        self.__tamanho -= 1
        self.__retrocederKPosições(1)

    def Buscar(self, chave: int) -> bool:
        """
        Manipula o `cursor` em busca de uma `chave` especifica.
        O `cursor` volta ao `inicio` caso não encontre o elemento.
        """
        if self.__inicio is None:
            return False
        fake = Elemento(chave)
        self.__fim.prox = fake

        iter = self.__inicio
        while iter.elemento != chave:
            iter = iter.prox

        if iter == fake:
            self.__irParaPrimeiro()
            self.__fim.prox = None
            return False

        else:
            self.__cursor = iter
            self.__fim.prox = None
            return True
        
    def mostra_lista(self):
        """
        Utiliza a função `print` para mostrar no terminal todos os elementos ***!!!sequencialmente!!!***.
        Em caso de lista vazia, mostrará "A lista está vazia!" no terminal.
        """
        iter = self.__inicio
        if iter == None:
            print('A lista está vazia!')
            return None
        else:
            print('| ', end='')
            while iter != None:
                print(iter.elemento, end=' | ')
                iter = iter.prox
            print()
    
    def num_elementos(self):
        """
        Retorna o numero de elementos da Lista.
        """
        return self.__tamanho

    
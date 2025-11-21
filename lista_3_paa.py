import sys
import heapq
from collections import deque
from typing import List, Tuple, Dict, Set

# sys.setrecursionlimit(200010)

##### ATENÇÃO #####
# Não altere o nome deste arquivo.
# Não altere a assinatura das funções.
# Não importe outros módulos além dos já importados.
# Você pode criar outras funções ou classes se julgar necessário, mas deve defini-las no corpo da função do exercicio.

# ==============================================================================
# Problema de exemplo
# ==============================================================================
def problema_0(n: int, m: int, A: List[Tuple[int, int]]) -> int:
    """
    Recebe um grafo com $n$ vertices numerados de $1$ a $n$ e m arestas
    bidirecionadas e retorna o número de componentes conexas do grafo.
    
    Complexidade: O(n + m)
    """

    # Podemos utilizar listas simples, ao invés de dicionários ou conjuntos, para 
    # representar o grafo, já que os vértices são numerados de 1 a n.
    # Isso economiza processamento e memória.
    visited = [False] * (n + 1)
    adj = [[] for _ in range(n + 1)] # lista de adjacência
	
    # Construindo o grafo
    for u, v in A:
        adj[u].append(v)
        adj[v].append(u)

    # No geral, dê preferência a BFS iterativa, pois é mais eficiente que a
    # DFS recursiva (principalmente em Python).
    def bfs(start: int):
        queue = deque([start]) # fila para BFS
        visited[start] = True

        while queue:
            u = queue.popleft() # nó atual

            for v in adj[u]: # vizinhos
                if not visited[v]:
                    visited[v] = True
                    queue.append(v)

    number_of_components = 0
    for u in range(1, n + 1):
        if not visited[u]:
            bfs(u)
            number_of_components += 1

    return number_of_components


# ==============================================================================
# Problema 1 - Sisi e a Sorveteria: Parte 2
# ==============================================================================

def problema_1(n: int, A: List[int]) -> int:
    """
    Desenvolva um algoritmo com complexidade $O(n)$ que encontre a quantidade
    máxima total de sorvete que Sisi pode obter.

    Entrada:
    A entrada consiste em uma lista de $n$ inteiros $A = [a_1, a_2,  dots, a_n]$,
    onde $a_i$ é o estoque do $i$-ésimo sorvete.

    Saída:
    Retorne um único inteiro $Q$, a quantidade máxima total de sorvete
    que Sisi pode obter.

    IDEIA: Como a quantidade de sorvete que posso pegar é estritamente menor que
    a quantidade que posso pegar do próximo sabor, então podemos fazer uma 
    escolha gulosa percorrendo a lista dos estoques do final para o início 
    """

    # Casos de bordo
    if n < 0 or A == []:
        return None

    # Função auxiliar para calcular o mínimo entre dois números
    def min(a, b):
        if a > b:
            return b
        else:
            return a

    n = len(A)
    quantidades = [0] * n  # Array de 0 para as quantidades de cada sorvete
    anterior = 1e9  # Definindo um comparador com limite da questão

    # Percorrendo a lista ao contrário
    for i in range(n-1, -1, -1):
        valor_comparacao = min(A[i], anterior - 1)  # Comparando o estoque do sabor atual com a quantidade escolhida anteriormente
        if valor_comparacao > 0:  # Sigo o comando da questão
            quantidades[i] = valor_comparacao
        anterior = quantidades[i]  # Atualizo a minha quantidade anterior

    return quantidades


# ==============================================================================
# Problema 2 - Minimizando Custos de Reparo
# ==============================================================================

def problema_2(n: int, k: int, C1: int, C2: int, A: List[int]) -> int:
    """
    Desenvolva um algoritmo com complexidade $O(k * log k)$ que encontre o
    custo mínimo para reparar a estrada.

    Entrada:
    - $n$: O expoente do comprimento da estrada ($L = 2^n$).
    - $C1$, $C2$: As constante de custo.
    - $A = [a_1, a_2,  dots, a_k]$: Uma lista com as $k$ posições dos buracos.

    Saída:
    - Retorne um único inteiro: o custo mínimo total para reparar toda a estrada.

    IDEIA: Vamos usar dividir e conquistar, mas ao invés de fazer só no intervalo 
    da estrada, vamos também fazer na lista de buracos.
    Dividimos normalmente o intervalo da estrada e depois dividimos o intervalo dos
    buracos com o seguinte raciocínio: qual o índice mais a direita do intervalo que 
    estou vendo que posso olhar para dividir, pois isso diminui o custo total
    """


    # Função auxiliar para, dada um array ordenado, retornar o índice mais a direita 
    # que um elemento x será adicionado na lista em O(logn)
    def adicionar_mais_a_direita(A, x):
        inicio = 0
        fim = len(A)  # Apesar de ser len(A), o intervalo é exclusivo
        while inicio < fim:
            meio = (inicio + fim) // 2
            if x < A[meio]:
                fim = meio
            else:
                inicio = meio + 1
        return inicio


    # Função auxiliar que resolve o problema para um intervalo [a,b]
    # dados os índices i e j da lista de buracos
    def solve_intervalo(a, b, i, j):

        l = b - a + 1  # Tamanho do intervalo
        N_b = j - i  # Número de buracos do intervalo
        custo_concerto_intervalo_todo = C2 * l * N_b  # Custo do intervalo com buracos
        
        # Caso em que não há buracos
        if N_b == 0:
            return C1

        # Caso em que não dá para dividir o intervalo em dois
        if l == 1:
            return custo_concerto_intervalo_todo
        
        # Achando o índice de divisão do intervalo
        meio = (a+b)//2
        idx_divisao = adicionar_mais_a_direita(A, meio)

        # Calculando os custos dos intervalos a esquerda e a direita
        custo_concerto_esq = solve_intervalo(a, meio, i, idx_divisao)
        custo_concerto_dir = solve_intervalo(meio+1, b, idx_divisao, j)
        custo_concerto_intervalo_dividido = custo_concerto_esq + custo_concerto_dir 

        return min(custo_concerto_intervalo_todo, custo_concerto_intervalo_dividido)


    A.sort()  # Garantir que está ordenado (klogk)
    L = 2**n  # Comprimento total

    # Passamos len(A) por conta do comportamento exclusivo de adicionar_mais_a_direita
    return solve_intervalo(1, L, 0, len(A))



# ==============================================================================
# Problema 3 - Subsequências radicais
# ==============================================================================

def problema_3(n: int, A: List[int]) -> int:
    """
    Desenvolva um algoritmo com complexidade $O(n * sqrt n)$ que retorne
    a quantidade de subsequências radicais.

    Entrada:
    - $A = [a_1, a_2,  dots, a_n]$ (com $1 <= a_i <= n$).

    Saída:
    - A quantidade total de subsequências radicais, módulo $999999937$.

    IDEIA: Vamos utilizar programação dinâmica e um dos princípios da estratégia
    gulosa. Primeiro, calculamos todos os divisores de um número em O(sqrt(n)) de
    forma ordenada (pela simetria do problema conseguimo fazer isso em O(sqrt(n)))
    Como a quantidade de divisores é da ordem de sqrt(n).
    Depois, criamos um array para armazenar quantas subsequências de tamanho i eu 
    tenho (incluíndo a sequência vazia, que é o caso base) e atualizamos o array de 
    subsequências
    """
    MOD = 999999937

    # Função auxiliar para calcular todos os divisores de um número em 
    # O(sqrt(número)) <= O(sqrt(n))
    def divisores_ordenados(num: int):
        divs_low = []
        divs_high = []
        upper_bound = min(num, n)
        r = int(pow(num, 1/2))
        for i in range(1, r + 1):
            if num % i == 0:
                if i <= upper_bound:
                    divs_low.append(i)
                if i != num // i and num//i <= upper_bound:   # divisor diferente
                    divs_high.append(num // i)
        return divs_high + divs_low
    
    # Definindo o array para guardar quantas subsequências de tamanho i eu tenho
    tamanho_subseqs = [0] * (n + 1)
    tamanho_subseqs[0] = 1 # tamanho_subseqs[0] = 1, representando a subsequência vazia (o ponto de partida)

    # Itera sobre cada elemento A[j] da sequência de entrada
    for a in A:
        # Pego os divisores do número a
        divisores = divisores_ordenados(a)
        
        # Para cada divisor k de 'a', o elemento 'a' pode ser o k-ésimo termo.
        # Iteramos do maior k para o menor.
        # Observe que len(divisores) <= sqrt(n) para {1} U [3, infty)
        for k in divisores:
            # Novo tamanho_subseqs[k] = tamanho_subseqs[k] + tamanho_subseqs[k-1]
            # O tamanho_subseqs[k-1] é o número de subsequências radicais de comprimento k-1
            # que a pode estender para formar novas subsequências de comprimento k.
            tamanho_subseqs[k] = tamanho_subseqs[k] + tamanho_subseqs[k-1]

    # O resultado é a soma de tamanho_subseqs, sem contar o caso da lista vazia
    total_radical_subsequences = sum(tamanho_subseqs) - 1

    return total_radical_subsequences % MOD
        

# ==============================================================================
# Problema 4 - Cavalo
# ==============================================================================

def problema_4(n: int) -> List[List[int]]:
    """
    Desenvolva um algoritmo com complexidade $O(n^2)$ que retorne
    a matriz de movimentos mínimos.

    Entrada:
    - $n$: O tamanho do lado do tabuleiro ($3   <= n   <= 10^3$).

    Saída:
    - Retorna uma matriz $A$, onde $A[i][j]$ é o número mínimo de
      movimentos para um cavalo ir da posição (i, j) para a posição (0, 0).

    IDEIA: Realizar um BFS na matriz, ou seja, supomos que a matriz é um grafo 
    com pesos iguais a 1 e encontramos o menor caminho do nó (casa do tabuleiro)
    até o "primeiro nó" ((0,0))
    """

    # Inicializa a matriz com -1 (não visitado) (O(n²)) e inicializa a fila para o BFS
    matriz = [[-1 for _ in range(n)] for _ in range(n)]
    matriz[0][0] = 0
    inicio = (0,0)
    queue = deque([inicio]) # fila para BFS

    # Realiza o BFS
    while queue:
        i, j = queue.popleft() # nó atual (popletft é O(1), enquanto pop(0) é O(n))
        movimentos_possiveis = [
            (i-2, j-1), (i-2, j+1), (i-1, j-2), (i-1, j+2),
            (i+1, j-2), (i+1, j+2), (i+2, j-1), (i+2, j+1)
        ]
        for novo_i, novo_j in movimentos_possiveis:
            # Verifica limites
            if 0 <= novo_i < n and 0 <= novo_j < n:  # Vê se a nova posição passou do tabuleiro
                if matriz[novo_i][novo_j] == -1:  # Vê se ainda não foi visitado
                    matriz[novo_i][novo_j] = matriz[i][j] + 1
                    queue.append((novo_i, novo_j))
    
    return matriz


# ==============================================================================
# Problema 5 - Escape se for possível
# ==============================================================================

def problema_5(n: int, m: int, grid: List[List[str]]) -> int:
    """
    Desenvolva um algoritmo com complexidade $O(n^2)$ que retorne
    o menor tempo para escapar.

    Entrada:
    - grid: Uma lista de listas de strings representando a caverna.

    Saída:
    - Retorne o menor tempo para escapar. Se não for possível, retorne -1.

    IDEIA: Fazer dois BFS. O primeiro seria para saber o tempo mínimo que água
    estaria numa célula (sem ser parede) do grid. O outro seria para saber o tempo
    mínimo em que eu estaria numa célula (sem ser parede ou água) do grid. 
    Faria a execução do segundo BFS até eu estar em uma das bordas da caverna.
    Caso não consiga, retornaria -1
    """

    INF = 10**7  # Infinito do problema
    VIZINHOS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Vetor de movimentos: Cima, Baixo, Esquerda, Direita

    # Inicializa a matriz com as posições das águas no tempo inicial
    # e coloca as posições das águas na fila
    matriz_tempo_agua = [[INF] * m for _ in range(n)]
    fila_agua = deque()    
    for r in range(n):
        for c in range(m):
            if grid[r][c] == 'A':
                matriz_tempo_agua[r][c] = 0
                fila_agua.append((r, c))

    # Inicializa a matriz com a minha posição inicial e coloca a minha
    # posição inicial na fila
    matriz_tempo_escape = [[INF] * m for _ in range(n)]
    fila_escape = deque()    
    for r in range(n):
        for c in range(m):
            if grid[r][c] == 'V':
                matriz_tempo_escape[r][c] = 0
                fila_escape.append((r, c))

    # Realizando o BFS na matriz de tempo das águas para saber o tempo mínimo
    # em que cada célula (diferente da parede) estará com água
    while fila_agua:
        i, j = fila_agua.popleft()
        tempo_agua_atual = matriz_tempo_agua[i][j]
        for di, dj in VIZINHOS:
            novo_i, novo_j = i + di, j + dj
            if 0 <= novo_i < n and 0 <= novo_j < m:  # Não passou da caverna
                if grid[novo_i][novo_j] != "#" and matriz_tempo_agua[novo_i][novo_j] == INF:  # Condições para atualizar o tempo
                    matriz_tempo_agua[novo_i][novo_j] = tempo_agua_atual + 1  # Atualizo o tempo mínimo
                    fila_agua.append((novo_i, novo_j))

    # Realizando  BFS na matriz de tempo de escape para saber o tempo mínimo
    # em que eu passo em cada célula (sem ser parede ou água)
    while fila_escape:
        i, j = fila_escape.popleft()
        tempo_escape_atual = matriz_tempo_escape[i][j]
        if i == 0 or i == n-1 or j == 0 or j == m-1:  # Se estou na borda (escapei)
            return tempo_escape_atual
        for di, dj in VIZINHOS:
            novo_i, novo_j = i + di, j + dj
            tempo_escape_novo = tempo_escape_atual + 1
            if 0 <= novo_i < n and 0 <= novo_j < m: # Não passou da caverna
                if grid[novo_i][novo_j] != "#" and matriz_tempo_escape[novo_i][novo_j] == INF and tempo_escape_novo < matriz_tempo_agua[novo_i][novo_j]: # Condições para atualizar o tempo
                    matriz_tempo_escape[novo_i][novo_j] = tempo_escape_novo  # Atualizo o tempo mínimo
                    fila_escape.append((novo_i, novo_j))

    # Não consegui escapar
    return -1 


# ==============================================================================
# Problema 6 - Viagem Intergalática
# ==============================================================================

def problema_6(n: int, m: int, rotas: List[Tuple[int, int, int]]) -> int:
    """
    Desenvolva um algoritmo com complexidade $O(m  log n)$ que retorne
    o custo mínimo total.

    Entrada:
    - $n$: Número de planetas ($1 <= n <= 10^5$).
    - $m$: Número de rotas ($1 <= m <= 2 * 10^5$).
    - rotas: Lista de $m$ tuplas $(a, b, c)$, onde $a$ é a origem,
      $b$ é o destino e $c$ é o custo.

    Saída:
    - Retorne o menor custo total possível para a viagem.
    """
    pass


# ==============================================================================
# Problema 7 - Reparo das Estradas
# ==============================================================================

def problema_7(n: int, m: int, estradas: List[Tuple[int, int, int]]) -> int:
    """
    Desenvolva um algoritmo com complexidade $O(m  log n)$ que retorne
    o custo mínimo total para conectar as cidades.

    Entrada:
    - $n$: Número de cidades ($1 <= n <= 10^5$).
    - $m$: Número de estradas ($1 <= m <= 2 * 10^5$).
    - estradas: Lista de $m$ tuplas $(a, b, c)$, onde $a$ e $b$ são
      cidades e $c$ é o custo do reparo.

    Saída:
    - Retorne o custo mínimo total para conectar todas as $n$ cidades.
    """
    pass


# ==============================================================================
# Problema 8 - Video Game
# ==============================================================================

def problema_8(n: int, m: int, transicoes: List[Tuple[int, int]]) -> int:
    """
    Desenvolva um algoritmo com complexidade $O(n + m)$ que encontre o número
    de formas distintas de ir do estado 1 ao estado $n$.

    Entrada:
    - $n$: O número de estados ($1 <= n <= 10^5$).
    - $m$: O número de transições ($1 <= m <= 2 * 10^5$).
    - transicoes: Uma lista com $m$ tuplas $(a, b)$ representando
      transições válidas.

    Saída:
    - Retorne um único inteiro: o número de formas distintas de ir do
      estado 1 ao estado $n$.
    """
    pass
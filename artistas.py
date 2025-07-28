
 # Importa a biblioteca CSV para trabalhar com arquivos CSV
import csv 

# Lista para armazenar os dados do CSV
dados = []



# Função que lê os dados do arquivo CSV e armazena na lista 'dados'.
# Toda vez que eu quiser carregar os dados do arquivo, basta chamar essa função.
def ler_dados():
    global dados
    with open('Spotify most streamed.csv', encoding='latin1') as arquivo: 
        leitor = csv.DictReader(arquivo)
           
        for linha in leitor: 
            
# Filtra para ignorar linhas com 'Various Artists -'
            if linha['Artist and Title'] != 'Various Artists -': 
                dados.append(linha)



# Esta função recebe um parâmetro, chamado texto.
# Esse parâmetro (texto) será o título que será exibido na tela (por exemplo, "Top 10 Artistas" ou "Análise de Streams").
def titulo(texto):

#Imprime um título formatado para as seções
    print()
    print(texto)
    print("-" * 40)



# Função que separa artista e música e converte streams para inteiros.
def tratar_dados():
    for linha in dados: 

# Separa artista e música
        artista_e_musica = linha['Artist and Title'].split(' - ', 1) # separador
        linha['artist_name'] = artista_e_musica[0].strip() if len(artista_e_musica) > 0 else ''
        linha['track_name'] = artista_e_musica[1].strip() if len(artista_e_musica) > 1 else ''
        
# Converte 'Streams' para inteiro, tratando erros
        try:
            linha['streams'] = int(linha['Streams'].replace(',', '').strip())
        except (ValueError, AttributeError):
            linha['streams'] = 0
        
# Converte 'Daily' (streams por dia) para inteiro, tratando erros
        try:
            linha['streams_per_day'] = int(linha['Daily'].replace(',', '').strip())
        except (ValueError, AttributeError):
            linha['streams_per_day'] = 0



# Esta função calcula e exibe os 10 artistas com mais streams totais.
def top_artistas():
    
    titulo("Top 10 Artistas com Mais Streams")
    
    artistas_streams = {} # Cria um dicionário vazio
    for linha in dados:
        artista = linha['artist_name']
        
# Soma streams de cada artista
        artistas_streams[artista] = artistas_streams.get(artista, 0) + linha['streams']
    
# Ordena do maior para o menor e pega os 10 primeiros
    top = sorted(artistas_streams.items(), key=lambda x: x[1], reverse=True)[:10]
    
# Imprime o ranking
    for i, (artista, streams) in enumerate(top, 1):
        print(f"{i:2d} - {artista}: {streams} streams")



# Esta função mostra as 10 músicas com mais streams totais e as 10 com mais streams por dia.
def top_musicas():

    titulo("Top 10 Músicas com Mais Streams Totais")
    top_total = sorted(dados, key=lambda x: x['streams'], reverse=True)[:10]
    
    for i, m in enumerate(top_total, 1):
        print(f"{i:2d} - {m['artist_name']} - {m['track_name']}: {m['streams']} streams")

    titulo("Top 10 Músicas com Mais Streams por Dia")
    top_dia = sorted(dados, key=lambda x: x['streams_per_day'], reverse=True)[:10]
    
    for i, m in enumerate(top_dia, 1):
        print(f"{i:2d} - {m['artist_name']} - {m['track_name']}: {m['streams_per_day']} streams/dia")




# Esta função compara o total de streams de dois artistas fornecidos pelo usuário.
def compara_artistas():

    titulo("Comparar Dois Artistas")
    a1 = input("Digite o nome do primeiro artista: ").strip().lower()
    a2 = input("Digite o nome do segundo artista: ").strip().lower()
    
# Soma os streams de cada artista
    s1 = sum(l['streams'] for l in dados if l['artist_name'].lower() == a1)
    s2 = sum(l['streams'] for l in dados if l['artist_name'].lower() == a2)
    
    print(f"\n{a1.title()}: {s1} streams")
    print(f"{a2.title()}: {s2} streams")
    
# Compara os resultados e imprime o vencedor ou empate
    if s1 > s2:
        print(f"{a1.title()} tem mais streams que {a2.title()}.")
    elif s2 > s1:
        print(f"{a2.title()} tem mais streams que {a1.title()}.")
    else:
        print("Ambos têm a mesma quantidade de streams.")



# Esta função encontra e imprime o artista e a música com mais streams por dia.
def artista_e_musica_mais_dia():

    titulo("Artista e Música com Mais Streams por Dia")
    
    artistas_por_dia = {}
    for l in dados:
        artistas_por_dia[l['artist_name']] = artistas_por_dia.get(l['artist_name'], 0) + l['streams_per_day']
    
    artista_mais = max(artistas_por_dia.items(), key=lambda x: x[1])
    musica_mais = max(dados, key=lambda x: x['streams_per_day'])
    
    print(f"Artista: {artista_mais[0]} - {artista_mais[1]} streams/dia")
    print(f"Música: {musica_mais['artist_name']} - {musica_mais['track_name']}: {musica_mais['streams_per_day']} streams/dia")




# Esta função calcula e mostra a operação de diferença entre a música com mais streams totais e a com mais streams por dia.
def diferenca_streams():

    titulo("Diferença entre a música com mais streams total e a mais streams por dia")
    
    musica_total = max(dados, key=lambda x: x['streams'])
    musica_dia = max(dados, key=lambda x: x['streams_per_day'])
    diff = musica_total['streams'] - musica_dia['streams_per_day']
    
    print(f"Música mais streams total: {musica_total['track_name']} com {musica_total['streams']} streams")
    print(f"Música mais streams por dia: {musica_dia['track_name']} com {musica_dia['streams_per_day']} streams/dia")
    print(f"Diferença: {diff}")




# Exibe o menu interativo e executa as funções conforme escolha do usuário.
def menu():

    ler_dados()
    tratar_dados()
    while True:
        titulo("Análise Spotify - Menu")
        print("1. Top 10 artistas com mais streams")
        print("2. Top 10 músicas (total e por dia)")
        print("3. Comparar dois artistas")
        print("4. Artista e música com mais streams por dia")
        print("5. Diferença entre músicas (total x por dia)")
        print("6. Sair")
        
        opc = input("Escolha uma opção: ").strip()
        
        if opc == '1':
            top_artistas()
        elif opc == '2':
            top_musicas()
        elif opc == '3':
            compara_artistas()
        elif opc == '4':
            artista_e_musica_mais_dia()
        elif opc == '5':
            diferenca_streams()
        elif opc == '6':
            print("Finalizando...")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    menu()

import pygame
from random import randint, choice
from math import inf

def inicializa():
    pygame.init()

    window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Jogo do Prady')

    assets = {}

    assets['pontuacao'] = []

    assets['lista_imagens'] = []
    for i in range(1, 17):
        assets['lista_imagens'].append(pygame.image.load(f'assets/img/img{i}.png'))

    assets['som_tiro'] = 'assets/snd/pew.wav'
    assets['som_tiro'] = pygame.mixer.Sound(assets['som_tiro'])
    assets['tela_atual'] = 'JOGO'

    state = {
        't0':-1,
        'last_updated': 0,
        'vidas': 3,
        'tempo_inicio': 0,
        'jogando': True
    }
    state['tempo_inicio'] = 0

    assets['imagens'] = []
    for i in range(5):
        assets['imagens'].append(sorteia_imagem(assets, state))

    # print(assets['imagens'])
    # print(assets['imagem_sorteada'])


    fonte = pygame.font.Font('assets/font/PressStart2P.ttf', 24)
    assets['fonte'] = fonte

    with open('ranking.txt', 'r') as file:
        texto = file.read()
        assets['pontuacao'] = texto.split()
        if len(assets['pontuacao']) > 10:
            min = +inf
            for e in assets['pontuacao']:
                if float(e) < min:
                    min = float(e)
            assets['pontuacao'].remove(str(min))


        # print(l)

    return window, assets, state



def sorteia_imagem(assets, state):
    dic = {}

    x = randint(0, 700)
    y = randint(-100, -25)
    vel = randint(1, 7)

    rand = randint(0, 15)
    dic['img'] = assets['lista_imagens'][rand]
    # print('lista_imagens', assets['lista_imagens'])
    dic['x'] = x
    dic['y'] = y
    dic['vel'] = vel
    if rand in (0, 2, 5, 7, 8, 10, 13, 15):
        dic['tipo'] = 'cachorro'
    else:
        dic['tipo'] = 'bagel'


    return dic

def atualiza_estado():
    # print(assets['tela_atual'])

    if assets['tela_atual'] == 'JOGO':
        # Calculo de variaçõa de tempo
        t0 = state['last_updated']
        t1 = pygame.time.get_ticks()
        t = (t1 - t0) / 1000
        state['last_updated'] = t1

        if state['vidas'] > 0:
            state['tempo_inicio'] += t



        coracoes = chr(9829) * state['vidas']
        assets['imagem_vidas'] = assets['fonte'].render(coracoes, True, (255, 0, 0))

        for imagem in assets['imagens']:
            imagem['y'] += imagem['vel']

            if imagem['y'] > 600:
                assets['imagens'].remove(imagem)
                assets['imagens'].append(sorteia_imagem(assets, state))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # print(state['tempo_inicio'])
                return False
            
            elif state['vidas'] <= 0:
                assets['tela_atual'] == 'RANKING'
                pontuacao_texto = assets['fonte'].render(f'Tempo: {int(state['tempo_inicio']):.2f}s', True, (255, 255, 255))
                state['pontuacao'] = pontuacao_texto
                state['jogando'] = False
                # with open('ranking.txt', 'a') as file:
                #     file.write(f'{state['tempo_inicio']:.2f}')
                #     file.close()
                # print(state['jogando'])

            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for imagem in assets['imagens']:
                    img_x, img_y = imagem['x'], imagem['y']
                    img_width, img_height = 100, 100

                    if img_x <= mouse_x <= mouse_x + img_width and img_y <= mouse_y <= img_y + img_height:
                        # print(imagem)

                        if img_x > 600 and imagem['tipo'] == 'cachorro':
                            state['vidas'] -= 1

                            if state['vidas'] <= 0:
                                assets['tela_atual'] = 'RANKING'

                            for k in range(2):
                                assets['imagens'].append(sorteia_imagem(assets, state))

                        if imagem['tipo'] == 'bagel':
                            assets['som_tiro'].play()
                            state['vidas'] -= 1
                            # print(state['vidas'])
                            for k in range(2):
                                assets['imagens'].append(sorteia_imagem(assets, state))
                        else:
                            assets['imagens'].remove(imagem)
                            assets['imagens'].append(sorteia_imagem(assets, state))

    # elif assets['tela_atual'] == 'RANKING':
    #     with open('ranking.txt', 'a') as file:
    #         file.write(f'{state['tempo_inicio']:.2f}')
    #         file.close()
    #     print(state['jogando'])

    return True
 

def desenha(window, assets): 


    window.fill((0, 0, 0))
    
    if state['jogando'] ==  True:
        for imagem in assets['imagens']:
            window.blit(pygame.transform.scale(imagem['img'], (100, 100)), (imagem['x'], imagem['y']))

        window.blit(pygame.transform.scale(assets['imagem_vidas'], (40, 30)), (720, 0))

        pontuacao_texto = assets['fonte'].render(f'Tempo: {int(state['tempo_inicio']):.2f}s', True, (255, 255, 255))
        window.blit(pontuacao_texto, (10, 10))
        pygame.display.update()

    else:
        pontuacao_atual = assets['fonte'].render('Pontuação atual:', True, (255, 255, 255))
        window.blit(pontuacao_atual, (100, 80))
        pontuacao_valor = assets['fonte'].render(f'{int(state['tempo_inicio']):.2f}', True, (255, 255, 255))
        window.blit(pontuacao_valor, (480, 80))
        ranking = assets['fonte'].render("Ranking:", True, (255, 255, 255))
        window.blit(ranking, (100, 130))
        y = 160
        for pontuacao in assets['pontuacao']:
            pontuacao_texto_ranking = assets['fonte'].render(pontuacao, True, (255, 255, 255))
            window.blit(pontuacao_texto_ranking,(200, y))
            y += 40
        # print(state['tempo_inicio'])
        pygame.display.update()

    pygame.display.update()
    return window

game = True

def game_loop(window, assets, state):
    while True:
        clock.tick(30)  

        if state['t0'] == -1:
            state['t0'] = pygame.time.get_ticks()

        if not atualiza_estado():
            return False
        
        # if state['vidas'] == 0:
        #     with open('ranking.txt', 'a') as file:
        #         file.write(f'{state['tempo_inicio']:.2f}')
        #         file.close()
        #     print(state['jogando'])
        desenha(window, assets)

if __name__ == "__main__":
    window, assets, state = inicializa()
    clock = pygame.time.Clock()

    ranking_updated = False  

    while game: 
        game = game_loop(window, assets, state)

        if state['vidas'] == 0 and not ranking_updated:  
            assets['tela_atual'] = 'RANKING'
            pontuacao_texto = assets['fonte'].render(f'Tempo: {int(state["tempo_inicio"])}s', True, (255, 255, 255))
            state['pontuacao'] = pontuacao_texto
            state['jogando'] = False

            with open('ranking.txt', 'w') as file:
                if not len(assets['pontuacao']) == 10:
                    assets['pontuacao'].append(f'{state['tempo_inicio']:.2f}')
                else:
                    min = +inf
                    for e in assets['pontuacao']:
                        if float(e) < min:
                            min = float(e)
                    if state['tempo_inicio'] > min:
                        assets['pontuacao'].append(f'{state['tempo_inicio']:.2f}')
                for pontuacao in assets['pontuacao']:
                    file.write(str(pontuacao))
                    file.write("\n")

            # with open('ranking.txt', 'r') as file:
            #     texto = file.read()
            #     l = texto.split()
            print(assets['pontuacao'])
            #     # for pontuacao in texto.split():
            #         # l = tex
            
            ranking_updated = True 

    pygame.quit()

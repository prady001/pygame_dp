import pygame
from random import randint, choice

def inicializa():
    pygame.init()

    window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Jogo do Prady')

    assets = {}
    assets['lista_imagens'] = []

    for i in range(1, 17):
        assets['lista_imagens'].append(pygame.image.load(f'assets/img/img{i}.png'))


    state = {
        't0':-1,
        'last_updated': 0,
        'vidas': 3,
    }

    assets['imagens'] = []
    for i in range(5):
        assets['imagens'].append(sorteia_imagem(assets, state))

    # print(assets['imagens'])
    # print(assets['imagem_sorteada'])


    fonte = pygame.font.Font('assets/font/PressStart2P.ttf', 12)
    assets['fonte'] = fonte

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

    # Calculo de variaçõa de tempo
    t0 = state['last_updated']
    t1 = pygame.time.get_ticks()
    t = (t1 - t0) / 1000
    state['last_updated'] = t1

    coracoes = chr(9829) * state['vidas']
    assets['imagem_vidas'] = assets['fonte'].render(coracoes, True, (255, 0, 0))

    for imagem in assets['imagens']:
        imagem['y'] += imagem['vel']

        if imagem['y'] > 600:
            assets['imagens'].remove(imagem)
            assets['imagens'].append(sorteia_imagem(assets, state))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or state['vidas'] == 0:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for imagem in assets['imagens']:
                img_x, img_y = imagem['x'], imagem['y']
                img_width, img_height = 100, 100

                if img_x <= mouse_x <= mouse_x + img_width and img_y <= mouse_y <= img_y + img_height:
                    print(imagem)
                    if imagem['tipo'] == 'bagel':
                        state['vidas'] -= 1
                        print(state['vidas'])
                        for k in range(2):
                            assets['imagens'].append(sorteia_imagem(assets, state))
                    else:
                        assets['imagens'].remove(imagem)
                        assets['imagens'].append(sorteia_imagem(assets, state))

    return True
 

def desenha(window, assets): 
    window.fill((0, 0, 0))

    for imagem in assets['imagens']:
        window.blit(pygame.transform.scale(imagem['img'], (100, 100)), (imagem['x'], imagem['y']))

    window.blit(pygame.transform.scale(assets['imagem_vidas'], (60, 30)), (720, 0))

    pygame.display.update()
    
    return window

game = True

def game_loop(window, assets, state):
    while True:
        clock.tick(30)  
        if not atualiza_estado():
            return False
        desenha(window, assets)

if __name__ == "__main__":
    window, assets, state = inicializa()
    clock = pygame.time.Clock()
    
    while game: 
        game = game_loop(window, assets, state)
    pygame.quit()

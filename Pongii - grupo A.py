# Para movimentar o Player:
# Use as teclas "Seta esquerda" para cima e "Seta direita" para baixo

import pygame
import random

pygame.init()

# Configurações da tela
screen = pygame.display.set_mode((800, 600))  # Define o tamanho da tela
pygame.display.set_caption("Pongii")  # Define o título da janela

# Cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# Posições e dimensões
ball_x, ball_y = 400, 300  # Posição inicial da bola
ball_dx, ball_dy = 5, 5  # Velocidade da bola
paddle1_x, paddle1_y = 50, 250  # Posição inicial do paddle1
paddle2_x, paddle2_y = 750, 250  # Posição inicial do paddle2
paddle_width, paddle_height = 10, 100  # Dimensões dos paddles

# Variáveis de velocidade
paddle1_speed = 5
paddle2_speed = 5
paddle1_moving_up = False
paddle1_moving_down = False
paddle2_moving_up = False
paddle2_moving_down = False

# Variáveis de controle de jogo
game_started = False  # Indica se o jogo começou
game_start_time = 0  # Tempo de início do jogo
clock = pygame.time.Clock()  # Relógio para controlar o FPS
font = pygame.font.Font(None, 74)  # Fonte para desenhar o texto na tela

# Função para resetar os elementos do jogo
def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, paddle1_y, paddle2_y, game_started, game_start_time
    ball_x, ball_y = 400, 300  # Reseta a posição da bola
    ball_dx, ball_dy = 5, 5  # Reseta a velocidade da bola
    paddle1_y, paddle2_y = 250, 250  # Reseta a posição dos paddles
    game_started = False  # Reseta o estado do jogo
    game_start_time = 0  # Reseta o tempo de início do jogo

# Função para desenhar o texto "START" no centro da tela
def draw_start_text():
    if pygame.time.get_ticks() // 500 % 2 == 0:  # Faz o texto piscar
        text = font.render("START", True, red)  # Renderiza o texto "START" na cor vermelha
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))  # Desenha o texto no centro da tela

# Loop principal do jogo
running = True

while running:
    # Tratamento de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Verifica se o usuário fechou a janela
            running = False
        elif event.type == pygame.KEYDOWN:  # Verifica se uma tecla foi pressionada
            if event.key == pygame.K_LEFT:  # Verifica se a tecla "Seta esquerda" foi pressionada
                paddle2_moving_up = True
                if not game_started:  # Inicia o jogo se ainda não tiver começado
                    game_started = True
                    game_start_time = pygame.time.get_ticks()  # Marca o tempo de início do jogo
            elif event.key == pygame.K_RIGHT:  # Verifica se a tecla "Seta direita" foi pressionada
                paddle2_moving_down = True
                if not game_started:  # Inicia o jogo se ainda não tiver começado
                    game_started = True
                    game_start_time = pygame.time.get_ticks()  # Marca o tempo de início do jogo
        elif event.type == pygame.KEYUP:  # Verifica se uma tecla foi solta
            if event.key == pygame.K_LEFT:  # Verifica se a tecla "Seta esquerda" foi solta
                paddle2_moving_up = False
            elif event.key == pygame.K_RIGHT:  # Verifica se a tecla "Seta direita" foi solta
                paddle2_moving_down = False

    # Lógica do jogo
    if game_started:
        current_time = pygame.time.get_ticks()
        if current_time - game_start_time >= 500:  # IA começa a funcionar depois de 500ms
            # IA Básica
            if random.random() < 0.050:  # chance de errar
                if ball_y + 15 > paddle1_y + paddle_height / 2:
                    paddle1_y -= paddle1_speed
                else:
                    paddle1_y += paddle1_speed
            else:  # chance de acertar
                if paddle1_y + paddle_height / 2 > ball_y:
                    paddle1_y -= paddle1_speed
                else:
                    paddle1_y += paddle1_speed

            # Colisão com os paddles
            if ball_y + 15 >= paddle1_y and ball_y <= paddle1_y + paddle_height:
                if ball_x <= paddle1_x + paddle_width and ball_x >= paddle1_x - 15:
                    ball_dx = -ball_dx  # Inverte a direção da bola
                    ball_x = paddle1_x + paddle_width + 1  # Ajusta a posição da bola

            if ball_y + 15 >= paddle2_y and ball_y <= paddle2_y + paddle_height:
                if ball_x >= paddle2_x - 15 and ball_x <= paddle2_x + paddle_width:
                    ball_dx = -ball_dx  # Inverte a direção da bola
                    ball_x = paddle2_x - 15 - 1  # Ajusta a posição da bola

            # Atualização da posição dos paddles
            if paddle1_y <= 0:
                paddle1_y = 0
            elif paddle1_y >= 500:
                paddle1_y = 500

            if paddle2_moving_up:
                paddle2_y -= paddle2_speed
            if paddle2_moving_down:
                paddle2_y += paddle2_speed

            if paddle2_y <= 0:
                paddle2_y = 0
            elif paddle2_y >= 500:
                paddle2_y = 500

            # Movimentação da bola
            ball_x += ball_dx
            ball_y += ball_dy

            if ball_y <= 0 or ball_y >= 590:
                ball_dy = -ball_dy  # Inverte a direção vertical da bola
            if ball_x <= 0 or ball_x >= 790:
                reset_game()  # Reseta o jogo se a bola sair pela lateral

    # Desenho dos elementos na tela
    screen.fill(black)  # Preenche a tela com a cor preta
    pygame.draw.rect(screen, blue, (paddle1_x, paddle1_y, paddle_width, paddle_height))  # Desenha o paddle1 na tela
    pygame.draw.rect(screen, green, (paddle2_x, paddle2_y, paddle_width, paddle_height))  # Desenha o paddle2 na tela
    pygame.draw.ellipse(screen, white, (ball_x, ball_y, 15, 15))  # Desenha a bola na tela
    for y in range(0, 600, 27):
        pygame.draw.rect(screen, white, (398, y, 4, 10))  # Desenha a linha pontilhada no centro da tela

    if not game_started:
        draw_start_text()  # Desenha o texto "START" no centro da tela se o jogo não começou

    pygame.display.flip()  # Atualiza a tela com o que foi desenhado
    clock.tick(60)  # Controla a taxa de atualização para 60 FPS

pygame.quit()  # Encerra o pygame
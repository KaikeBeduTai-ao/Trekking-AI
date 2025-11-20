import pygame


class GameWindow:
    def __init__(self, width=640, height=480):
        # Ajustei o tamanho padrão para 640x480 para bater com a webcam padrão,
        # assim a posição X do mouse/objeto fica 1:1 com a câmera.
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Trekking AI - Radar")
        self.font = pygame.font.SysFont("Arial", 18)

    def update(self, object_pos=None, zone_limits=None):
        """
        object_pos: Tupla (x, y) do centro do objeto rastreado.
        zone_limits: Tupla (limite_esq, limite_dir) das linhas verticais.
        """
        # 1. Limpa a tela (Fundo Cinza Escuro)
        self.screen.fill((30, 30, 30))

        width, height = self.screen.get_size()

        # 2. Desenha as Zonas (Linhas Verticais)
        if zone_limits:
            lim_esq, lim_dir = zone_limits

            # Área Esquerda (Levemente Vermelha)
            # pygame.draw.rect(self.screen, (40, 30, 30), (0, 0, lim_esq, height))

            # Área Direita (Levemente Vermelha)
            # pygame.draw.rect(self.screen, (40, 30, 30), (lim_dir, 0, width - lim_dir, height))

            # Área Central (Levemente Verde - Zona Segura)
            pygame.draw.rect(self.screen, (30, 50, 30),
                             (lim_esq, 0, lim_dir - lim_esq, height))

            # Linhas divisórias
            pygame.draw.line(self.screen, (200, 200, 200),
                             (lim_esq, 0), (lim_esq, height), 2)
            pygame.draw.line(self.screen, (200, 200, 200),
                             (lim_dir, 0), (lim_dir, height), 2)

            # Labels
            lbl_esq = self.font.render("ESQUERDA", True, (100, 100, 100))
            lbl_dir = self.font.render("DIREITA", True, (100, 100, 100))
            lbl_cen = self.font.render("FRENTE", True, (100, 200, 100))

            self.screen.blit(lbl_esq, (10, 10))
            self.screen.blit(lbl_dir, (width - 80, 10))
            self.screen.blit(lbl_cen, (width//2 - 30, 10))

        # 3. Desenha o Objeto Rastreado (Círculo Laranja)
        if object_pos:
            x, y = object_pos
            # Desenha um alvo
            pygame.draw.circle(self.screen, (255, 150, 0),
                               (x, y), 10)  # O ponto
            pygame.draw.circle(self.screen, (255, 150, 0),
                               (x, y), 20, 2)  # O aro

        pygame.display.flip()

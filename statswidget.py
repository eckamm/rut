class StatsWidget:
    def __init__(self):
        self.cps = 0
        self.cpc = 1
        self.cookies = 0
        self.game_cookies = 0
        self._font = pygame.font.SysFont(None, 15)

    def update(self, lifetime, current):
        self.lifetime = lifetime
        self.current = current

    def draw(self, surface):
        """
        """
        cps_render = self._font.render("DPS: %s" % fmt(self.cps), True, (255,255,255))
        cps_box = cps_render.get_rect()
        cps_box.left = 10
        cps_box.centery = 20
        surface.blit(cps_render, cps_box)

        cpc_render = self._font.render("DPC: %s" % fmt(self.cpc), True, (255,255,255))
        cpc_box = cpc_render.get_rect()
        cpc_box.left = 10
        cpc_box.top = cps_box.bottom + 10
        surface.blit(cpc_render, cpc_box)

        cookies_render = self._font.render("Donuts: %s" % fmt(self.cookies), True, (255,255,255))
        cookies_box = cookies_render.get_rect()
        cookies_box.left = 10
        cookies_box.top = cpc_box.bottom + 10
        surface.blit(cookies_render, cookies_box)

        game_cookies_render = self._font.render("Total Donuts: %s" % fmt(self.game_cookies), True, (255,255,255))
        game_cookies_box = game_cookies_render.get_rect()
        game_cookies_box.left = 10
        game_cookies_box.top = cookies_box.bottom + 10
        surface.blit(game_cookies_render, game_cookies_box)

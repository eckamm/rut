"""

      D         O         N         U        T

   X boxes   X boxes   X boxes   X boxes  X boxes

    [Play]    [Play]    [Play]    [Play]   [Play]


Scene returns the profile_idx to use or None to quit.


"""
try:
    import android
except ImportError:
    android = None

from common import *
from fonts import Fonts
from backgroundwidget import BackgroundWidget
from buttonwidget import ButtonWidget



def profiles_scene(screen, save_jdat):

    background_widget = BackgroundWidget()

    img_files = [
        DONUT_RED_IMAGE,
        DONUT_ORANGE_IMAGE,
        DONUT_YELLOW_IMAGE,
        DONUT_GREEN_IMAGE,
        DONUT_BLUE_IMAGE,
    ]

    antialias = True
    color = THECOLORS["white"]
    x = SCREEN_WIDTH//6
    y = 3*SCREEN_HEIGHT//4
    ctrl = []
    for profile, img_file in zip(save_jdat["profiles"], img_files):
        letter = profile["name"]
        shards = "%s box" % (fmt(profile["lifetime"]["shards"]),)
        if profile["lifetime"]["shards"] != 1:
            shards += "es"
        donut_img = pygame.image.load(os.path.join(GAMEDIR, img_file)).convert_alpha()
        donut_img = pygame.transform.smoothscale(donut_img, (128, 128))
        donut_box = donut_img.get_rect()
        donut_box.center = (x, 300)
        text1_render = getattr(Fonts, "f80").render(letter, antialias, color)
        text1_box = text1_render.get_rect()
        text1_box.center = (x, 185)
        text2_render = getattr(Fonts, "f20").render(shards, antialias, color)
        text2_box = text2_render.get_rect()
        text2_box.center = (x, 400)
        ctrl.append([
            donut_img, donut_box,
            text1_render, text1_box,
            text2_render, text2_box,
            ButtonWidget(os.path.join(GAMEDIR, BUTTON_PLAY_IMAGE)),
        ])
        tmp = ctrl[-1][-1].box
        tmp.center = (x, 440)
        ctrl[-1][-1].box = tmp
        x += SCREEN_WIDTH//6


    clock = pygame.time.Clock()
    running = True
    while running:

        if android:
            if android.check_pause():
                print "@@@@ pausing"
                running = False

        ms_elapsed = clock.tick(TICK)
        elapsed = ms_elapsed/1000.0

        # Events...
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ret_val = None   # None means quit
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                ret_val = None   # None means quit
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                # Removing this key action will also disable the Android "back" button.
                ret_val = None   # None means quit
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFTBUTTON:
                for idx, (donut_img, donut_box, text1, box1, text2, box2, button) in enumerate(ctrl):
                    if button.on_click(event.pos):
                        ret_val = idx
                        running = False

        # Updating...
        for donut_img, donut_box, text1, box1, text2, box2, button in ctrl:
            button.update(elapsed)

        # Drawing...
        background_widget.draw(screen)
        for donut_img, donut_box, text1, box1, text2, box2, button in ctrl:
            screen.blit(donut_img, donut_box)
            screen.blit(text1, box1)
            screen.blit(text2, box2)
            button.draw(screen)

        pygame.display.flip()
        pygame.event.pump()

    return ret_val



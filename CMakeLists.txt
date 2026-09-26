# Loaded as a Zephyr module (zephyr/module.yml). Only adds the OLED status
# screen, and only when config/sofle.conf selects the custom screen.
target_sources_ifdef(CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM app PRIVATE src/status_screen.c)

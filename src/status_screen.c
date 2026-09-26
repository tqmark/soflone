/*
 * OLED status screen: ZMK's built-in screen minus the keyboard icon before
 * the layer name. The icon is hard-coded in ZMK's layer widget and the light
 * UNSCII 8 font has no glyph for it, so this screen draws the name as plain
 * text. Battery and output icons reuse ZMK's own widgets, laid out as before.
 *
 * SPDX-License-Identifier: MIT
 */

#include <zephyr/kernel.h>

#include <zmk/display.h>
#include <zmk/display/status_screen.h>
#include <zmk/display/widgets/battery_status.h>
#include <zmk/display/widgets/output_status.h>
#include <zmk/event_manager.h>
#include <zmk/events/layer_state_changed.h>
#include <zmk/keymap.h>

static struct zmk_widget_battery_status battery_status_widget;
static struct zmk_widget_output_status output_status_widget;
static lv_obj_t *layer_label;

struct layer_name_state {
    zmk_keymap_layer_index_t index;
    const char *name;
};

static void layer_name_update_cb(struct layer_name_state state) {
    if (layer_label == NULL) {
        return;
    }

    if (state.name == NULL || state.name[0] == '\0') {
        char text[4] = {};

        snprintf(text, sizeof(text), "%u", state.index);
        lv_label_set_text(layer_label, text);
    } else {
        lv_label_set_text(layer_label, state.name);
    }
}

static struct layer_name_state layer_name_get_state(const zmk_event_t *eh) {
    zmk_keymap_layer_index_t index = zmk_keymap_highest_layer_active();

    return (struct layer_name_state){
        .index = index, .name = zmk_keymap_layer_name(zmk_keymap_layer_index_to_id(index))};
}

ZMK_DISPLAY_WIDGET_LISTENER(widget_layer_name, struct layer_name_state, layer_name_update_cb,
                            layer_name_get_state)

ZMK_SUBSCRIPTION(widget_layer_name, zmk_layer_state_changed);

lv_obj_t *zmk_display_status_screen() {
    lv_obj_t *screen = lv_obj_create(NULL);

    zmk_widget_battery_status_init(&battery_status_widget, screen);
    lv_obj_align(zmk_widget_battery_status_obj(&battery_status_widget), LV_ALIGN_TOP_RIGHT, 0, 0);

    zmk_widget_output_status_init(&output_status_widget, screen);
    lv_obj_align(zmk_widget_output_status_obj(&output_status_widget), LV_ALIGN_TOP_LEFT, 0, 0);

    layer_label = lv_label_create(screen);
    lv_obj_set_style_text_font(layer_label, lv_theme_get_font_small(screen), LV_PART_MAIN);
    lv_obj_align(layer_label, LV_ALIGN_BOTTOM_LEFT, 0, 0);
    widget_layer_name_init();

    return screen;
}

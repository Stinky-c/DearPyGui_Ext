from datetime import datetime
import dearpygui.dearpygui as dpg

class mvLogger:

    def __init__(self, parent=None,**kwargs):
        """when supplied kwargs, unpack into dpg.window"""

        self.log_level = 0
        self._auto_scroll = True
        self.filter_id = None
        if parent:
            self.window_id = parent
        else:
            if kwargs:
                self.window_id = dpg.add_window(**kwargs)
            else:
                self.window_id = dpg.add_window(label="mvLogger", pos=(200, 200), width=500, height=500)
        self.count = 0
        self.flush_count = 1000

        with dpg.group(horizontal=True, parent=self.window_id):
            dpg.add_checkbox(label="Auto-scroll", default_value=True, callback=lambda sender:self.auto_scroll(dpg.get_value(sender)))
            dpg.add_button(label="Clear", callback=lambda: dpg.delete_item(self.filter_id, children_only=True))

        dpg.add_input_text(label="Filter", callback=lambda sender: dpg.set_value(self.filter_id, dpg.get_value(sender)), 
                    parent=self.window_id)
        self.child_id = dpg.add_child_window(parent=self.window_id, autosize_x=True, autosize_y=True)
        self.filter_id = dpg.add_filter_set(parent=self.child_id)


        with dpg.theme() as self.debug_theme:
            with dpg.theme_component(0):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (64, 128, 255, 255)) # blue

        with dpg.theme() as self.info_theme:
            with dpg.theme_component(0):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255)) # white

        with dpg.theme() as self.warning_theme:
            with dpg.theme_component(0):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 0, 255)) # yellow

        with dpg.theme() as self.error_theme:
            with dpg.theme_component(0):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 0, 0, 255)) # red

        with dpg.theme() as self.critical_theme:
            with dpg.theme_component(0):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 0, 0, 255)) # red

    def auto_scroll(self, value):
        self._auto_scroll = value

    def _log(self, message, level):

        if level < self.log_level:
            return

        self.count+=1

        if self.count > self.flush_count:
            self.clear_log()

        theme = self.info_theme

        # removed trace and update formatting
        match level:
            case 1:
                message = f"[{datetime.now().strftime('%H:%M:%S')}] [DEBUG]    {message}"
                theme = self.debug_theme
            case 2:
                message = f"[{datetime.now().strftime('%H:%M:%S')}] [INFO]    {message}"
                theme = self.info_theme
            case 3:
                message = f"[{datetime.now().strftime('%H:%M:%S')}] [WARNING]    {message}"
                theme = self.warning_theme
            case 4:
                message = f"[{datetime.now().strftime('%H:%M:%S')}] [ERROR]    {message}"
                theme = self.error_theme
            case 5:
                message = f"[{datetime.now().strftime('%H:%M:%S')}] [CRITICAL]    {message}"
                theme = self.critical_theme

        new_log = dpg.add_text(message, parent=self.filter_id, filter_key=message)
        dpg.bind_item_theme(new_log, theme)
        if self._auto_scroll:
            scroll_max = dpg.get_y_scroll_max(self.child_id)
            dpg.set_y_scroll(self.child_id, -1.0)


    def debug(self, message):
        self._log(message, 1)

    def info(self, message):
        self._log(message, 2)

    def warning(self, message):
        self._log(message, 3)

    def error(self, message):
        self._log(message, 4)

    def critical(self, message):
        self._log(message, 5)

    def clear_log(self):
        dpg.delete_item(self.filter_id, children_only=True)
        self.count = 0

#! /usr/bin/python3.4
# -*- coding: utf-8 -*-
#
# program.py
#

import os
import sys
import string

from random import choice

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import ConfigParser

from libs.uix import customsettings
from libs.uix.dialogs import dialog

from libs.uix.kv.activity.baseclass.startscreen import StartScreen
from libs.uix.kv.activity.baseclass.introduction import Introduction
from libs.uix.kv.activity.baseclass.createaccount import CreateAccount
from libs.uix.kv.activity.baseclass.addaccount import AddAccount
from libs.uix.kv.activity.baseclass.addaccountown import AddAccountOwn

from libs import programdata as data
from libs import programclass as _class

from kivymd.theming import ThemeManager
from kivymd.bottomsheet import MDGridBottomSheet
# from kivymd.navigationdrawer import NavigationDrawer


# class NavDrawer(NavigationDrawer):
#     events_callback = ObjectProperty()


class Program(App, _class.ShowPlugin, _class.ShowAbout, _class.ShowLicense):
    '''Функционал программы.'''

    settings_cls = customsettings.CustomSettings
    customsettings.TEXT_INPUT = data.string_lang_enter_value
    # nav_drawer = ObjectProperty()
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Green'

    def __init__(self, **kvargs):
        super(Program, self).__init__(**kvargs)
        Window.bind(on_keyboard=self.events_program)

        self.data = data
        self.window = Window
        self.open_exit_dialog = None
        self.load_all_kv_files('{}/libs/uix/kv'.format(self.directory))
        self.load_all_kv_files(
            '{}/libs/uix/kv/activity'.format(self.directory)
        )
        self.bottom_sheet_content = {
            'Add account':
                ['Settings', lambda x: None, 'data/images/settings.png']
        }

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'language', 'Русский')
        config.setdefault('General', 'theme', 'default')

    def build_settings(self, settings):
        with open('{}/data/settings/general.json'.format(
                data.prog_path), 'r') as settings_json:
            settings.add_json_panel(data.string_lang_settings, self.config,
                data=settings_json.read().format(
                    language=data.string_lang_setting_language,
                    title=data.string_lang_setting_language_title,
                    desc=data.string_lang_setting_language_desc,
                    russian=data.string_lang_setting_language_russian,
                    english=data.string_lang_setting_language_english))

    def build(self):
        self.use_kivy_settings = False
        self.title = data.string_lang_title  # заголовок окна программы
        self.icon = 'data/images/logo.png'  # иконка окна программы

        self.config = ConfigParser()
        self.config.read('{}/program.ini'.format(data.prog_path))

        # Главный экран программы.
        # self.screen = StartScreen(events_callback=self.events_program)
        self.screen = StartScreen()
        self.screen_root_manager = self.screen.ids.root_manager
        # self.nav_drawer = NavDrawer(title=data.string_lang_menu)

        return self.screen

    def events_program(self, *args):
        '''Вызывается при выборе одного из пунктов меню программы.'''

        if len(args) == 2:  # нажата ссылка
            event = args[1]
        else:  # нажата кнопка программы
            try:
                _args = args[0]
                event = _args if isinstance(_args, str) else _args.id
            except AttributeError:  # нажата кнопка девайса
                event = args[1]

        if data.PY2:
            if isinstance(event, unicode):
                event = event.encode('utf-8')

        if event == data.string_lang_settings:
            self.open_settings()
        elif event == data.string_lang_exit_key:
            self.exit_program()
        elif event == data.string_lang_license:
            self.show_license()
        elif event == data.string_lang_plugin:
            self.show_plugins()
        elif event in (1001, 27):
            self.back_screen(event)
        elif event in (282, 319):
            self.show_bottom_sheet()
        elif event == 'About':
            self.show_about()

        return True

    def back_screen(self, name_screen):
        '''Менеджер экранов.'''

        name_current_screen = self.screen_root_manager.current

        # Нажата BackKey.
        if name_screen in (1001, 27):
            if name_current_screen == 'Start screen':
                self.exit_program()
                return
            else:
                self.screen_root_manager.current = 'Start screen' \
                    if name_current_screen == 'Add account own provider' \
                    else self.screen_root_manager.previous()
                return

        self.screen_root_manager.current = 'Start screen' \
            if name_current_screen == 'Add account own provider' \
            else name_screen

    def exit_program(self, *args):
        def close_dialog():
            self.open_exit_dialog.dismiss()
            self.open_exit_dialog = None

        if self.open_exit_dialog:
            return

        self.open_exit_dialog = dialog(
            text=data.string_lang_exit, title=self.title, dismiss=False,
            buttons=[
                [data.string_lang_yes, lambda *x: sys.exit(0)],
                [data.string_lang_no, lambda *x: close_dialog()]
            ]
        )

    def load_all_kv_files(self, directory_kv_files):
        for kv_file in os.listdir(directory_kv_files):
            if kv_file == 'bugreporter.kv' or os.path.isdir('{}/{}'.format(
                    directory_kv_files, kv_file)):
                continue
            Builder.load_file('{}/{}'.format(directory_kv_files, kv_file))

    def show_bottom_sheet(self):
        current_name_screen = self.screen_root_manager.current
        bottom_sheet = MDGridBottomSheet()

        if current_name_screen in self.bottom_sheet_content:
            name_item, callback, icon = \
                self.bottom_sheet_content[current_name_screen]
            bottom_sheet.add_item(name_item, callback, icon_src=icon)
            bottom_sheet.open()

    def delete_textfield_and_set_check_in_addaccountroot(self):
        add_account_own_provider = self.screen.ids.add_account_own_provider
        add_account_root = add_account_own_provider.ids.add_account_root
        add_account_root.ids.check.active = False
        add_account_root.ids.box.remove_widget(
            add_account_root.ids.confirm_password
        )

    def set_focus_on_textfield(self, interval=0, instance_textfield=None, focus=True):
        if instance_textfield:
            instance_textfield.focus = focus

    def check_len_login_in_textfield(self, instance_textfield):
        if len(instance_textfield.text) > 20:
                instance_textfield.text = instance_textfield.text[:20]
        instance_textfield.message = 'username@conversations.im' \
            if instance_textfield.text == '' \
            else '{}@conversations.im'.format(instance_textfield.text)

    def set_text_on_textfields(self, interval):
        add_account_root = self.screen.ids.add_account.ids.add_account_root
        field_username = add_account_root.ids.username
        field_password = add_account_root.ids.password
        field_confirm_password = add_account_root.ids.confirm_password

        field_username.text = self.screen.ids.create_account.ids.username.text.lower()
        field_password.focus = True
        password = self.generate_password()
        field_password.text = password
        field_confirm_password.text = password

        Clock.schedule_once(
            lambda x: self.set_focus_on_textfield(
                instance_textfield=field_password, focus=False), .5
        )
        Clock.schedule_once(
            lambda x: self.set_focus_on_textfield(
                instance_textfield=field_username), .5
        )

    def generate_password(self):
        for x in range(1):
            return ''.join([choice(string.ascii_lowercase + string.digits)
                            for i in range(8)])

    def on_config_change(self, config, section, key, value):
        '''Вызывается при выборе одного из пункта настроек программы.'''

        if key == 'language':
            if not os.path.exists('{}/data/language/{}.txt'.format(
                    self.directory, data.select_locale[value])):
                dialog(
                    text=data.string_lang_not_locale.format(
                         data.select_locale[value]), title=self.title
                )
                config.set(section, key, data.old_language)
                config.write()
                self.close_settings()

    def on_pause(self):
        '''Ставит приложение на 'паузу' при выхоже из него.
        В противном случае запускает программу заново.'''

        return True

    def on_stop(self):
        '''Вызывается при выходе из прилодения.'''

        pass

from kivy.uix.screenmanager import Screen


class AddAccountOwn(Screen):

    def _on_enter(self, instance_toolbar, instance_program, instance_screenmanager):
        instance_toolbar.title = instance_program.data.string_lang_add_account
        instance_field_username = self.ids.add_account_root.ids.username
        instance_field_username.message = 'username@conversations.im'
        instance_field_username.message_mode = 'persistent'
        instance_field_username.focus = True

        instance_toolbar.left_action_items = [
            ['chevron-left', lambda x: instance_program.back_screen(
                instance_screenmanager.previous())]
        ]

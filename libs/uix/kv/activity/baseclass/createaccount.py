from kivy.uix.screenmanager import Screen


class CreateAccount(Screen):

    def _on_enter(self, instance_toolbar, instance_program, instance_screenmanager):
        instance_toolbar.title = instance_program.data.string_lang_create_account
        instance_toolbar.left_action_items = [
            ['chevron-left', lambda x: instance_program.back_screen(
                instance_screenmanager.previous())]
        ]

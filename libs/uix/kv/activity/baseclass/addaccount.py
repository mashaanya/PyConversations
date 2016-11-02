from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


class AddAccount(Screen):

    def _on_enter(self, instance_toolbar, instance_program):
        instance_toolbar.title = self.name
        self.ids.add_account_root.ids.username.focus = True
        Clock.schedule_once(instance_program.set_text_on_textfields, .5)

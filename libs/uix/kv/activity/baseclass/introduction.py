from kivy.uix.screenmanager import Screen


class Introduction(Screen):

    def _on_enter(self, instance_toolbar, instance_program):
        instance_toolbar.left_action_items = []
        instance_toolbar.title = instance_program.title

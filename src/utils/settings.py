import gradio as gr


class Settings_UI:

    def sidebar(state):

        state = not state

        return gr.update(visible=state),state
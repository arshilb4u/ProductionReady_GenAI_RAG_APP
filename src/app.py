import gradio as gr
from utils.settings import Settings_UI

with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.TabItem("GPT WITH RAG"):
            with gr.Row() as row:
                with gr.Column(visible=False) as ref_bar:
                    ref = gr.Markdown()
        
                with gr.Column() as chat_output:
                    chatbot = gr.Chatbot(
                        [],
                        elem_id = "chatbot",
                        bubble_full_width=False,
                        height=500
                        )
            with gr.Row():
                input_text = gr.Textbox(
                    lines=4,
                    scale=8,
                    placeholder ="Please Enter you message here...",
                    container =False
                )
            with gr.Row() as row_last:
                submit_button = gr.Button(value="Submit Button")
                sidebar_state = gr.State(False)
                btn_toggle_sidebar = gr.Button(value="References")
                btn_toggle_sidebar.click(Settings_UI.sidebar, [sidebar_state], [
                    ref_bar, sidebar_state])
                upload_btn = gr.UploadButton(
                    "Upload PDF file", file_types=['.pdf'],file_count="multiple")
                rag_with_dropdown = gr.Dropdown(label="RAG with", choices=["Preprocessed doc", "Upload doc: Process for RAG", "Upload doc: Give Full summary"], value="Preprocessed doc")
                clear_button = gr.ClearButton([input_text, chatbot])



demo.launch()

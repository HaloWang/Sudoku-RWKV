import gradio as gr

def sudoku_ui():
    with gr.Row():
        for i in range(9):
            with gr.Row():
                for j in range(9):
                    gr.Textbox(
                        label="",
                        placeholder="",
                        lines=1,
                        max_lines=1,
                        interactive=True,
                        visible=True,
                        container=False
                    )

# 主 Gradio 界面
with gr.Blocks() as demo:
    with gr.Box():
        gr.Markdown("### 数独游戏")
        sudoku_ui()  # 调用数独 UI 模块化组件

demo.launch()

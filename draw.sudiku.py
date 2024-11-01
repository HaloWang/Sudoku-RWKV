import gradio as gr
from PIL import Image, ImageDraw, ImageFont


def draw_sudoku_board(board, cell_size=50):
    size = cell_size * 9
    img = Image.new("RGB", (size, size), color="white")
    draw = ImageDraw.Draw(img)

    # 绘制网格线
    for i in range(10):
        line_width = 3 if i % 3 == 0 else 1
        draw.line((i * cell_size, 0, i * cell_size, size), fill="black", width=line_width)
        draw.line((0, i * cell_size, size, i * cell_size), fill="black", width=line_width)

    # 在每个单元格中绘制数字
    font = ImageFont.load_default()  # 使用默认字体
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:  # 非零值表示预设数字
                x = j * cell_size + cell_size // 4
                y = i * cell_size + cell_size // 4
                draw.text((x, y), str(board[i][j]), fill="black", font=font)

    return img


# 初始化一个数独棋盘
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Gradio 界面
with gr.Blocks() as demo:
    gr.Markdown("### 数独游戏棋盘")
    gr.Image(value=draw_sudoku_board(sudoku_board), label="数独棋盘")

demo.launch()

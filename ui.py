import copy

import gradio as gr
from PIL import Image, ImageDraw, ImageFont
import time

from generate_sudoku_data import generate_sudoku
from launch import parse_output_content, solve_sudoku_using_model, check_cot


def draw_sudoku_board(board, cell_size=33):
    
    if board is None:
        board = empty_board
    
    size = cell_size * 9
    img = Image.new("RGB", (size, size), color="white")
    draw = ImageDraw.Draw(img)

    # Draw grid lines
    for i in range(10):
        line_width = 3 if i % 3 == 0 else 1
        draw.line((i * cell_size, 0, i * cell_size, size), fill="black", width=line_width)
        draw.line((0, i * cell_size, size, i * cell_size), fill="black", width=line_width)

    # Draw numbers in each cell
    font = ImageFont.load_default(16)  # Use default font
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:  # Non-zero values indicate preset numbers
                x = j * cell_size + cell_size // 4
                y = i * cell_size + cell_size // 4
                draw.text((x, y), str(board[i][j]), fill="black", font=font, align="center")
    return img


# Initialize an empty Sudoku board
empty_board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

ui_difficulty = 1
ui_base_seed = None
ui_current_seed = ui_base_seed if ui_base_seed is not None else int(time.time())
default_max_token_count = 500000
break_when_something_wrong = False


def generate_puzzle():
    global ui_current_seed
    puzzle, puzzle_solved = generate_sudoku(difficulty=ui_difficulty, seed=ui_current_seed)
    ui_current_seed = ui_base_seed if ui_base_seed is not None else int(time.time())

    return puzzle, puzzle_solved


def solve_puzzle(current_puzzle, current_resolution):
    logger, is_completed = solve_sudoku_using_model(copy.deepcopy(current_puzzle),
                                                    verbose=True,
                                                    max_token_count=default_max_token_count,
                                                    real_time_verification=break_when_something_wrong)
    if is_completed:
        cot = logger.log
        success = check_cot(current_puzzle, current_resolution, cot, verify_intermediate_step=False, verbose=False)
        if success:
            print("✅ success")
        else:
            print("❌ failed")
        return get_result_from_cot(cot)
    return empty_board


def get_result_from_cot(cot):
    split_cot = cot.split("<check state>")
    split_cot = [x.strip() for x in split_cot]
    split_cot.pop(0)
    output = split_cot.pop(-1)
    print("✅ output: ", output)
    mp_answer_exist, mp_answer = parse_output_content(output + '</output>')
    print("✅ mp_answer: ", mp_answer)
    return mp_answer


def update_grid_left(puzzle):
    return draw_sudoku_board(puzzle)


def update_grid_right(puzzle):
    return draw_sudoku_board(puzzle)

def update_grid_llm_resolution(puzzle):
    return draw_sudoku_board(puzzle)

# Gradio interface
with gr.Blocks() as demo:
    current_puzzle = gr.State(empty_board)
    current_resolution = gr.State(empty_board)
    llm_resolution = gr.State(empty_board)

    gr.Markdown("# RWKV Sudoku CoT Demo")

    gr.Button("Generate Sudoku puzzle").click(fn=generate_puzzle, outputs=[current_puzzle, current_resolution])

    with gr.Row():
        grid_left = gr.Image(value=draw_sudoku_board(current_puzzle.value), label="Current Puzzle")
        grid_right = gr.Image(value=draw_sudoku_board(current_resolution.value), label="Current Resolution")

    current_puzzle.change(fn=update_grid_left, inputs=current_puzzle, outputs=grid_left)
    current_resolution.change(fn=update_grid_right, inputs=current_resolution, outputs=grid_right)

    gr.Button("Resolve current puzzle").click(
        fn=solve_puzzle,
        inputs=[current_puzzle, current_resolution],
        outputs=[llm_resolution])
    
    with gr.Row():
        grid_llm_resolution = gr.Image(value=draw_sudoku_board(llm_resolution.value), label="LLM Resolution")
        
    llm_resolution.change(fn=update_grid_llm_resolution, inputs=llm_resolution, outputs=grid_llm_resolution)

demo.launch()

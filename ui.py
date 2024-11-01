from generate_sudoku_data import generate_sudoku

import copy
import time
from launch import default_difficulty, ui_current_seed, solve_sudoku_using_model, default_max_token_count, break_when_something_wrong, check_cot

import gradio as gr

ui_base_seed = None
ui_grid = None
ui_solved_grid = None

ui_current_seed = ui_base_seed if ui_base_seed is not None else int(time.time())

def generate():
    print("✅ Generating")
    global ui_grid, ui_solved_grid, ui_current_seed, ui_base_seed

    ui_grid, ui_solved_grid = generate_sudoku(difficulty=1, seed=ui_current_seed)
    ui_current_seed = ui_base_seed if ui_base_seed is not None else int(time.time())

    return ui_grid, ui_solved_grid

def solve():
    print("✅ Solving")
    global ui_grid, ui_solved_grid, ui_current_seed, ui_base_seed

    if ui_grid is None:
        print("❌ Grid is None")
        return

    print("✅ ui_grid: ", ui_grid)
    print("✅ ui_solved_grid: ", ui_solved_grid)

    logger, is_completed = solve_sudoku_using_model(copy.deepcopy(ui_grid), 
                                                    verbose=True, 
                                                    max_token_count=default_max_token_count, 
                                                    real_time_verification=break_when_something_wrong)
    if is_completed:
        cot = logger.log
        success = check_cot(ui_grid, ui_solved_grid, cot, verify_intermediate_step=False, verbose=True)
    return

def sudoku_ui(array):
    # 生成一个用于数独的 UI 模块
    sudoku_elements = []
    with gr.Row():
        for i in range(9):
            with gr.Column(scale=1):
                row_elements = []
                for j in range(9):
                    cell = gr.Textbox(value=array[i][j] if array[i][j] != 0 else "", interactive=True, label=None)
                    row_elements.append(cell)
                sudoku_elements.append(row_elements)
    return sudoku_elements

def update_ui():
    global ui_grid, ui_solved_grid, ui_current_seed, ui_base_seed
    print("✅ Updating UI")
    if ui_grid is None:
        print("❌ ui_grid is None")
        return []
    return sudoku_ui(ui_grid)

with gr.Blocks() as demo:

    grid_text = gr.Textbox(label="Grid")

    solved_grid_text = gr.Textbox(label="Solved Grid")

    generate_btn = gr.Button("Generate a new sudoku puzzle")
    generate_btn.click(fn=generate, outputs=[grid_text, solved_grid_text])

    # Dynamically update the UI based on the grid
    grid_ui = gr.State(value=None)
    generate_btn.click(fn=update_ui, outputs=grid_ui)

    if ui_grid is not None:
        sudoku_ui(ui_grid)

    solve_btn = gr.Button("Solve")
    solve_btn.click(fn=solve, inputs=[], outputs=[])

if __name__ == "__main__":
    demo.launch()

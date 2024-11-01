from generate_sudoku_data import generate_sudoku

import copy
import time
from launch import ui_current_seed, solve_sudoku_using_model, default_max_token_count, break_when_something_wrong, check_cot

import gradio as gr

ui_base_seed = None
ui_grid = None
ui_solved_grid = None
ui_difficulty = 1
ui_current_seed = ui_base_seed if ui_base_seed is not None else int(time.time())

def generate_puzzle():
    print("✅ Generating a new puzzle")
    global ui_grid, ui_solved_grid, ui_current_seed, ui_base_seed

    ui_grid, ui_solved_grid = generate_sudoku(difficulty=ui_difficulty, seed=ui_current_seed)
    ui_current_seed = ui_base_seed if ui_base_seed is not None else int(time.time())

    return ui_grid, ui_solved_grid

def solve_puzzle():
    print("✅ Solving the current puzzle")
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
    # Create a button to generate the puzzle
    generate_button = gr.Button("Generate Puzzle")
    
    # Create a textbox to display the Sudoku grid or a message
    sudoku_output = gr.Textbox(label="Sudoku Grid", interactive=False)
    
    # Define the function to update the UI with the generated puzzle
    def update_sudoku_ui():
        if ui_grid is None: return "No puzzle generated yet."
        with gr.Row() as row:
            btn1 = gr.Button("Button 1")
            btn2 = gr.Button("Button 2")
        return row
    
    # Set up the button click event to generate the puzzle and update the UI
    generate_button.click(fn=generate_puzzle, outputs=[sudoku_output])
    generate_button.click(fn=update_sudoku_ui, outputs=[sudoku_output])

if __name__ == "__main__":
    demo.launch()

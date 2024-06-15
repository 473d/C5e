import tkinter as tk
from tkinter import Canvas, messagebox
from PIL import Image, ImageDraw, ImageTk
import pytesseract
import numpy as np

# Initialize Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Path to your Tesseract executable

# Function to recognize characters from drawn image using OCR
def recognize_characters(image):
    text = pytesseract.image_to_string(image, config='--psm 6')  # --psm 6 for treating image as a uniform block of text
    return text.strip()

# Function to handle mouse movements and drawing on canvas
def on_mouse_drag(event):
    global last_x, last_y
    canvas.create_line((last_x, last_y, event.x, event.y), width=5, fill='black')
    draw.line((last_x, last_y, event.x, event.y), fill='black', width=5)
    last_x, last_y = event.x, event.y

def on_mouse_down(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y

def on_mouse_up(event):
    pass

# Function to process the drawn image and solve equation
def process_equation():
    # Get the drawn image from the canvas
    bbox = canvas.bbox("all")
    drawn_image = Image.new('RGB', (bbox[2], bbox[3]), 'white')
    drawn_image.paste(canvas_image, (-bbox[0], -bbox[1]))

    # Optionally, you might want to preprocess the image before OCR
    processed_image = drawn_image.convert('L')  # Convert to grayscale

    # Recognize characters using OCR
    equation_text = recognize_characters(processed_image)

    # Print recognized equation (for debugging)
    print("Recognized equation:", equation_text)

    # Here, you would implement code to parse and solve the equation
    # Example: evaluating a simple expression (you would need a proper parser for complex equations)
    try:
        solution = eval(equation_text)
        messagebox.showinfo("Solution", f"Solution: {solution}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to solve equation: {str(e)}")

# Create the main application window
root = tk.Tk()
root.title("Equation Solver")

# Create a canvas widget for drawing
canvas = Canvas(root, width=600, height=400, bg='white')
canvas.pack()

# Create an image for drawing (using PIL)
canvas_image = Image.new('RGB', (600, 400), 'white')
draw = ImageDraw.Draw(canvas_image)

# Bind mouse events to canvas
canvas.bind("<B1-Motion>", on_mouse_drag)
canvas.bind("<Button-1>", on_mouse_down)
canvas.bind("<ButtonRelease-1>", on_mouse_up)

# Create Solve button
solve_button = tk.Button(root, text="Solve", command=process_equation)
solve_button.pack()

# Run the application
root.mainloop()

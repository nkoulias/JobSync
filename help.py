import streamlit as st
from google.cloud import vision
from sympy import symbols, Eq, solve, sympify, Function, dsolve
from sympy.parsing.sympy_parser import parse_expr
from PIL import Image
import io
import re

# Set up Google Cloud Vision client
def get_vision_client():
    # Specify the path to your service account key file
    client = vision.ImageAnnotatorClient.from_service_account_json('C:\\Users\\Nick Koulias\\Downloads\\strange-passage-424220-m8-6389fb7aafbd.json')
    return client

# OCR function using Google Cloud Vision
def extract_text_from_image(image):
    client = get_vision_client()
    # Convert the image to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    image_bytes = buffered.getvalue()
    
    # Prepare the image for the API request
    image = vision.Image(content=image_bytes)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    # Print the full response for debugging
    print(f"Full OCR Response: {response}")
    return texts[0].description if texts else ""

# Replace superscript characters with their corresponding values
def replace_superscripts(text):
    superscripts = {
        '²': '**2',
        '³': '**3',
        '⁴': '**4',
        '⁵': '**5',
        '⁶': '**6',
        '⁷': '**7',
        '⁸': '**8',
        '⁹': '**9',
        '⁰': '**0'
    }
    for sup, value in superscripts.items():
        text = text.replace(sup, value)
    return text

# Add multiplication signs where needed
def add_multiplication_signs(text):
    text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)  # 2x -> 2*x
    text = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', text)  # x2 -> x*2
    return text

# Clean and preprocess the extracted text
def preprocess_extracted_text(text):
    # Remove unwanted characters and spaces
    cleaned_text = text.replace('\n', '').replace(' ', '').strip()
    # Replace common OCR errors and ensure basic equation format
    cleaned_text = replace_superscripts(cleaned_text)
    cleaned_text = add_multiplication_signs(cleaned_text)
    return cleaned_text

# Generate steps for solving algebraic equations
def generate_algebraic_steps(eq, x):
    steps = []
    # Simplify the equation
    simplified_eq = eq.simplify()
    steps.append(f"Step 1: Simplify both sides of the equation (if necessary). Simplified equation: {simplified_eq}")
    
    # Move all terms to one side to set the equation to zero
    if simplified_eq.lhs != 0:
        isolated_eq = Eq(simplified_eq.lhs - simplified_eq.rhs, 0)
        steps.append(f"Step 2: Move all terms to one side to set the equation to zero: {isolated_eq}")
    else:
        isolated_eq = simplified_eq
    
    # Isolate the variable
    if isolated_eq.lhs.has(x):
        steps.append(f"Step 3: Isolate the variable x.")
        steps.append(f"Start with: {isolated_eq}")
        solutions = solve(isolated_eq, x)
        for sol in solutions:
            steps.append(f"x = {sol}")
    
    return steps, solutions

# Generate steps for solving differential equations
def generate_differential_steps(eq, func):
    steps = []
    steps.append(f"Solving the differential equation: {eq}")
    solution = dsolve(eq, func)
    steps.append(f"Solution: {solution}")
    return steps, [solution]

# Solve the mathematical problem using SymPy
def solve_math_problem(equation_str):
    x = symbols('x')
    y = Function('y')(x)
    try:
        # Ensure the equation is in the correct format
        equation_str = preprocess_extracted_text(equation_str)
        equation_parts = equation_str.split('=')
        if len(equation_parts) != 2:
            return ["Error: The extracted text does not appear to be a valid equation."], []

        # Parse the equation parts and create the equation
        left_side = sympify(equation_parts[0])
        right_side = sympify(equation_parts[1])
        print(f"Parsed Left Side: {left_side}")  # Debugging statement
        print(f"Parsed Right Side: {right_side}")  # Debugging statement
        equation = Eq(left_side, right_side)
        
        # Determine if the equation is differential or algebraic
        if equation.has(y.diff(x)):
            # Differential equation
            steps, solutions = generate_differential_steps(equation, y)
        else:
            # Algebraic equation
            steps, solutions = generate_algebraic_steps(equation, x)
        
        return steps, solutions
    except SyntaxError as e:
        return [f"SyntaxError: {e}"], []
    except Exception as e:
        return [f"Error: {e}"], []

# Streamlit app
st.title("Math Problem Solver with Google Cloud Vision and SymPy")
st.write("Upload an image of a math problem, and I'll solve it for you!")

uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg", "tiff"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Extract text from the image
    extracted_text = extract_text_from_image(image)
    st.write(f"Extracted Text: {extracted_text}")
    print(f"Extracted Text: {extracted_text}")  # Print to console for debugging
    
    # Solve the math problem
    steps, solutions = solve_math_problem(extracted_text.strip())
    for step in steps:
        st.write(step)
    st.write(f"Solutions: {solutions}")

# Run the app with: streamlit run app.py

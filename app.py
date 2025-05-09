import os
from dotenv import load_dotenv
import requests
import google.generativeai as genai
from fuzzywuzzy import fuzz

# Load environment variables from .env file
load_dotenv()

# Fetch API key (ensure your .env uses the key name GOOGLE_API_KEY)
api_key = os.getenv("GOOGLE_API_KEY")

print(f"Loaded API Key: '{api_key}'")  


if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

# Configure Google Gemini AI with your API key
genai.configure(api_key=api_key)

def get_products():
    """Fetch products from the mock API."""
    url = "https://5d76bf96515d1a0014085cf9.mockapi.io/product"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching products: {e}")
        return None

def call_gemini_api(prompt):
    """Call Gemini API with a given prompt."""
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        # Check if response contains text, otherwise convert to string
        return response.text if hasattr(response, "text") else str(response)
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Error communicating with Gemini API."

def get_gemini_response(user_input, products):
    """Find relevant products and get a response from Gemini AI."""
    relevant_products = []
    user_words = user_input.lower().split()

    # Direct keyword matching
    for product in products:
        product_name = product.get('name', '').lower()
        product_description = product.get('description', '').lower()
        if any(word in product_name or word in product_description for word in user_words):
            relevant_products.append(product)

    # Fuzzy matching if no direct matches found
    if not relevant_products:
        for product in products:
            name_similarity = fuzz.ratio(user_input.lower(), product.get('name', '').lower())
            description_similarity = fuzz.ratio(user_input.lower(), product.get('description', '').lower())
            if name_similarity > 60 or description_similarity > 40:
                relevant_products.append(product)

    # Construct prompt for Gemini API
    if relevant_products:
        prompt = f"User query: {user_input}\n\nMatching Products:\n"
        for product in relevant_products:
            prompt += (
                f"- **{product.get('name')}**: {product.get('description')} "
                f"(Price: ${product.get('price')})\n"
            )
        prompt += "\nProvide a helpful response based on these products."
    else:
        prompt = f"User query: {user_input}\nNo relevant products found. Provide an alternative response."

    return call_gemini_api(prompt)

def chat_with_bot(user_input):
    """Process user input and return chatbot response."""
    products = get_products()
    if not products:
        return "Sorry, I couldn't fetch product details."
    return get_gemini_response(user_input, products)

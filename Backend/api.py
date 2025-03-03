from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os
from datetime import datetime
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = "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"

def get_temperature(response_mode):
    """Get temperature based on response mode."""
    temperatures = {
        "accurate": 0.2,
        "normal": 0.7,
        "creative": 1.2
    }
    # Default to normal if mode is invalid
    temp = temperatures.get(response_mode.lower(), 0.7)
    logger.info(f"Temperature for mode {response_mode}: {temp}")
    return temp

def validate_mode(mode, valid_modes, default_mode="normal"):
    """Validate the mode and return a default if invalid."""
    # Check if mode is a string
    if not isinstance(mode, str):
        logger.warning(f"Invalid mode type: {type(mode)}, using default: {default_mode}")
        return default_mode
        
    mode = mode.strip().lower()
    
    if not mode:
        logger.warning(f"Empty mode provided, using default: {default_mode}")
        return default_mode
        
    if mode not in valid_modes:
        logger.warning(f"Invalid mode: {mode}, using default: {default_mode}")
        return default_mode
        
    logger.info(f"Valid mode: {mode}")
    return mode

def process_prompt(message, explanation_mode="normal", response_mode="normal"):
    """Process and enhance the user's prompt based on selected modes."""
    
    # Validate modes
    valid_explanation_modes = {"normal", "friendly"}
    valid_response_modes = {"accurate", "normal", "creative"}
    
    explanation_mode = validate_mode(explanation_mode, valid_explanation_modes, "normal")
    response_mode = validate_mode(response_mode, valid_response_modes, "normal")
    
    logger.info(f"Processing prompt with modes - Explanation: {explanation_mode}, Response: {response_mode}")
    
    # Base system message
    system_message = "You are a helpful AI tutor designed specifically for students. "
    
    # Add explanation mode context
    if explanation_mode == "friendly":
        system_message += "Explain concepts in simple terms that a 10 year old child can understand. Use analogies and examples from everyday life. "
    else:
        system_message += "Provide clear, well-structured explanations suitable for students. "
    
    # Add response mode context
    if response_mode == "creative":
        system_message += "Be creative and imaginative in your responses, exploring different possibilities and perspectives. "
    elif response_mode == "accurate":
        system_message += "Focus on accuracy and precision, providing factual and well-researched information. "
    else:  # normal mode
        system_message += "Maintain a balance between accuracy and creativity, providing informative yet engaging responses. "
    
    # Add general guidelines
    system_message += "Break down complex topics into digestible parts and encourage critical thinking."
    
    return {
        "role": "system",
        "content": system_message
    }

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        logger.info(f"Received request data: {json.dumps(data)}")
        
        user_message = data.get("message", "").strip()
        explanation_mode = data.get("explanationMode", "normal")
        response_mode = data.get("responseMode", "normal")
        
        logger.info(f"Processing request - Message: {user_message[:50]}..., Explanation Mode: {explanation_mode}, Response Mode: {response_mode}")
        
        if not user_message:
            return jsonify({
                "error": "Message cannot be empty",
                "timestamp": datetime.now().isoformat()
            }), 400

        # Get processed system message
        system_message = process_prompt(user_message, explanation_mode, response_mode)
        
        # Get temperature based on response mode
        temperature = get_temperature(response_mode)
        
        logger.info(f"Using temperature: {temperature} for response mode: {response_mode}")

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000"
        }

        payload = {
            "model": "openai/gpt-4o",  # Updated model name to a valid one
            "messages": [
                system_message,
                {"role": "user", "content": user_message}
            ],
            "temperature": temperature,
            "max_tokens": 800
        }

        logger.info(f"Sending request to OpenRouter with payload: {json.dumps(payload)}")

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        logger.info(f"Received response from OpenRouter: Status {response.status_code}")
        
        if response.status_code != 200:
            error_msg = f"API returned status code {response.status_code}"
            logger.error(f"{error_msg} - Response: {response.text}")
            return jsonify({
                "error": error_msg,
                "details": response.text,
                "timestamp": datetime.now().isoformat()
            }), 500
        
        api_response = response.json()
        
        if 'choices' not in api_response or not api_response['choices']:
            error_msg = "Invalid response structure from API"
            logger.error(f"{error_msg} - Response: {json.dumps(api_response)}")
            return jsonify({
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            }), 500
        
        bot_message = api_response['choices'][0]['message']['content']
        
        final_response = {
            "success": True,
            "response": bot_message,
            "timestamp": datetime.now().isoformat(),
            "modes": {
                "explanation": explanation_mode,
                "response": response_mode,
                "temperature": temperature
            }
        }
        
        logger.info("Successfully processed request and sending response")
        return jsonify(final_response)

    except requests.exceptions.RequestException as e:
        error_msg = f"Failed to communicate with OpenRouter API: {str(e)}"
        logger.error(f"{error_msg}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response content: {e.response.text}")
        
        return jsonify({
            "error": error_msg,
            "timestamp": datetime.now().isoformat()
        }), 500
    
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        logger.error(f"{error_msg}")
        return jsonify({
            "error": error_msg,
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
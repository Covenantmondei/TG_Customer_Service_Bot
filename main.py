import os
import logging
from typing import Dict, Any, Optional, Union
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Telegram Customer Support Bot")

# Get credentials from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Telegram API URLs
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


# Pydantic models for request validation
class TelegramUpdate(BaseModel):
    update_id: int
    message: Optional[Dict[str, Any]] = None


# FAQ responses - easy to extend
FAQ_RESPONSES = {
    "hours": "Our business hours are Monday to Friday, 9 AM to 6 PM EST. We're closed on weekends and public holidays.",
    "location": "We're located at 123 Main Street, Suite 100, New York, NY 10001. You can also reach us online 24/7!",
    "contact": "You can contact us via:\n📧 Email: support@company.com\n📞 Phone: +1 (555) 123-4567\n💬 This chat (24/7 AI support)",
    "shipping": "We offer free shipping on orders over $50. Standard shipping takes 3-5 business days, and express shipping takes 1-2 business days.",
    "returns": "We accept returns within 30 days of purchase. Items must be unused and in original packaging. Contact us to initiate a return.",
    "payment": "We accept all major credit cards, PayPal, Apple Pay, and Google Pay. All transactions are secure and encrypted.",
}


# Helper Functions
def check_faq(message_text: str) -> Optional[str]:
    """
    Check if the message matches any FAQ keywords.
    Returns the FAQ answer if found, None otherwise.
    """
    message_lower = message_text.lower()
    
    for keyword, response in FAQ_RESPONSES.items():
        if keyword in message_lower:
            logger.info(f"FAQ match found for keyword: {keyword}")
            return response
    
    return None


def get_ai_response(user_message: str) -> str:
    """
    Generate a customer support response using OpenAI API.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can change to "gpt-4" if you have access
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful and friendly customer support agent. "
                        "Provide clear, concise, and professional responses to customer inquiries. "
                        "Be empathetic and solution-oriented. Keep responses under 200 words."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        ai_reply = response.choices[0].message.content.strip()
        logger.info("AI response generated successfully")
        return ai_reply
    
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        return "I apologize, but I'm having trouble processing your request right now. Please try again in a moment or contact our support team directly."


def send_telegram_message(chat_id: int, text: str) -> bool:
    """
    Send a message to a Telegram chat using the Bot API.
    """
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info(f"Message sent successfully to chat_id: {chat_id}")
        return True
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending message to Telegram: {e}")
        return False


def process_message(message: Dict[str, Any]) -> None:
    """
    Process an incoming message and send an appropriate response.
    """
    # Extract message details
    chat_id = message.get("chat", {}).get("id")
    message_text = message.get("text", "")
    user_name = message.get("from", {}).get("first_name", "there")
    
    if not chat_id or not message_text:
        logger.warning("Received message without chat_id or text")
        return
    
    logger.info(f"Processing message from {user_name} (chat_id: {chat_id}): {message_text}")
    
    # Check for /start command
    if message_text.startswith("/start"):
        welcome_message = (
            f"👋 Hello {user_name}! Welcome to our customer support.\n\n"
            "I'm here to help you 24/7. You can ask me about:\n"
            "• Business hours\n"
            "• Location\n"
            "• Contact information\n"
            "• Shipping & returns\n"
            "• Payment options\n"
            "• Or anything else!\n\n"
            "How can I assist you today?"
        )
        send_telegram_message(chat_id, welcome_message)
        return
    
    # Check FAQ first
    faq_response = check_faq(message_text)
    
    if faq_response:
        # Send FAQ response
        send_telegram_message(chat_id, faq_response)
    else:
        # Generate AI response
        ai_response = get_ai_response(message_text)
        send_telegram_message(chat_id, ai_response)


# API Endpoints
@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Telegram Customer Support Bot",
        "version": "1.0.0"
    }


@app.get("/set_webhook")
def set_webhook(webhook_url: str):
    """
    Set the webhook URL for the Telegram bot.
    
    Example: GET /set_webhook?webhook_url=https://your-domain.com/webhook
    """
    url = f"{TELEGRAM_API_URL}/setWebhook"
    payload = {"url": webhook_url}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        logger.info(f"Webhook set successfully: {webhook_url}")
        return {
            "success": True,
            "message": "Webhook set successfully",
            "webhook_url": webhook_url,
            "telegram_response": result
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error setting webhook: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to set webhook: {str(e)}")


@app.post("/webhook")
async def webhook(request: Request):
    """
    Handle incoming updates from Telegram.
    """
    try:
        # Parse the incoming update
        update_data = await request.json()
        logger.info(f"Received update: {update_data}")
        
        # Extract message from update
        message = update_data.get("message")
        
        if message:
            # Process the message
            process_message(message)
        else:
            logger.warning("Received update without a message")
        
        return {"status": "ok"}
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        # Return 200 to prevent Telegram from retrying
        return {"status": "error", "message": str(e)}


@app.get("/webhook_info")
def get_webhook_info():
    """
    Get current webhook information from Telegram.
    """
    url = f"{TELEGRAM_API_URL}/getWebhookInfo"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        return {
            "success": True,
            "webhook_info": result.get("result", {})
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting webhook info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get webhook info: {str(e)}")


# For local development and testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
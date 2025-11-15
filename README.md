# Telegram Customer Support AI Agent

A FastAPI-powered Telegram bot that provides intelligent customer support using OpenAI's GPT models. The bot can handle common FAQs instantly and uses AI to respond to complex customer inquiries.

## Features

- **Instant FAQ Responses**: Predefined answers for common questions (hours, location, contact, shipping, returns, payment)
- **AI-Powered Support**: OpenAI GPT integration for handling complex customer queries
- **Webhook-Based**: Efficient webhook implementation for real-time message handling
- **Easy to Extend**: Modular code structure with clear helper functions
- **Production-Ready**: Comprehensive error handling and logging
- **Secure**: Environment variable management for sensitive credentials

## Prerequisites 

- Python 3.8 or higher
- A Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- An OpenAI API Key (from [OpenAI Platform](https://platform.openai.com/))
- A public URL for webhook (deployment server or ngrok for testing)

## Installation 

1. **Clone the repository**
   ```powershell
   git clone https://github.com/Covenantmondei/TG_Customer_Service_Bot.git
   cd TG_Customer_Service_Bot
   ```

2. **Create a virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```plaintext
   BOT_TOKEN=your_telegram_bot_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage 

### Running Locally

1. **Start the FastAPI server**
   ```powershell
   uvicorn main:app --reload
   ```
   
   The server will start at `http://localhost:8000`

2. **Test the health endpoint**
   ```powershell
   curl http://localhost:8000
   ```

### Setting Up the Webhook

#### Option 1: Using ngrok (for testing)

1. **Install ngrok** from [ngrok.com](https://ngrok.com/)

2. **Start ngrok tunnel**
   ```powershell
   ngrok http 8000
   ```

3. **Set the webhook** (replace with your ngrok URL)
   ```
   GET https://your-ngrok-url.ngrok.io/set_webhook?webhook_url=https://your-ngrok-url.ngrok.io/webhook
   ```

#### Option 2: Production Deployment

1. Deploy to a hosting service (Heroku, Railway, Render, DigitalOcean, etc.)

2. Set the webhook with your production URL:
   ```
   GET https://your-domain.com/set_webhook?webhook_url=https://your-domain.com/webhook
   ```

### Verifying Webhook Status

Check if your webhook is properly configured:
```
GET https://your-domain.com/webhook_info
```

## API Endpoints 

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check endpoint |
| `GET` | `/set_webhook` | Register webhook with Telegram |
| `POST` | `/webhook` | Handle incoming Telegram messages |
| `GET` | `/webhook_info` | Get current webhook information |

## Bot Commands 

Users can interact with the bot using these commands:

- `/start` - Welcome message and bot introduction

## FAQ Keywords 

The bot automatically detects these keywords and provides instant responses:

- **hours** - Business hours information
- **location** - Physical location details
- **contact** - Contact information (email, phone)
- **shipping** - Shipping policies and timeframes
- **returns** - Return policy details
- **payment** - Accepted payment methods

## Customization 

### Adding More FAQ Responses

Edit the `FAQ_RESPONSES` dictionary in `main.py`:

```python
FAQ_RESPONSES = {
    "hours": "Your custom hours response",
    "your_keyword": "Your custom response",
    # Add more...
}
```

### Changing the AI Model

Modify the OpenAI model in the `get_ai_response()` function:

```python
response = client.chat.completions.create(
    model="gpt-4",  # Change to gpt-4 or other models
    # ...
)
```

### Customizing AI Behavior

Edit the system prompt in `get_ai_response()` function:

```python
{
    "role": "system",
    "content": "Your custom system prompt here..."
}
```

## Project Structure 

```
Tg_Bot/
│
├── main.py              # Main application code
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in git)
├── .gitignore          # Git ignore rules
├── README.md           # This file
└── __pycache__/        # Python cache (not in git)
```

## Dependencies 

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-dotenv` - Environment variable management
- `openai` - OpenAI API client
- `requests` - HTTP library for Telegram API
- `pydantic` - Data validation

## Environment Variables 

| Variable | Description | Required |
|----------|-------------|----------|
| `BOT_TOKEN` | Your Telegram Bot Token from @BotFather | Yes |
| `OPENAI_API_KEY` | Your OpenAI API Key | Yes |

## Deployment Options 

### Heroku

```powershell
heroku create your-app-name
heroku config:set BOT_TOKEN=your_token
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

### Railway

1. Connect your GitHub repository
2. Add environment variables in Railway dashboard
3. Deploy automatically

### Render

1. Create a new Web Service
2. Connect your repository
3. Add environment variables
4. Deploy

## Troubleshooting 

### Bot not responding

1. Check if webhook is set correctly:
   ```
   GET /webhook_info
   ```

2. Verify environment variables are loaded:
   - Check `.env` file exists
   - Ensure no extra spaces in variable values

3. Check server logs for errors

### OpenAI API errors

- Verify your API key is valid and has credits
- Check if you have access to the specified model (gpt-3.5-turbo or gpt-4)
- Monitor rate limits

### Webhook errors

- Ensure your URL is publicly accessible (HTTPS required for production)
- Check if the webhook URL matches your server URL
- Telegram requires HTTPS for webhooks (ngrok provides this automatically)

## Security Best Practices 

- ✅ Never commit `.env` file to version control
- ✅ Keep your API keys secure
- ✅ Use HTTPS for production webhooks
- ✅ Regularly rotate your API keys
- ✅ Monitor API usage and costs

## Contributing 

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 

This project is open source and available under the [MIT License](LICENSE).

## Support 

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [@Covenantmondei](https://github.com/Covenantmondei)

## Acknowledgments 

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [OpenAI](https://openai.com/) - AI API
- [Telegram Bot API](https://core.telegram.org/bots/api) - Messaging platform

---

**Note**: Remember to keep your `.env` file secure and never share your API keys publicly!
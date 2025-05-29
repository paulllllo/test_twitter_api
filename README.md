# Twitter OAuth2 Demo

This is a FastAPI application that demonstrates Twitter OAuth2 authentication and posting tweets using the Twitter API v2.

## Setup

1. Create a Twitter Developer Account and create a new project/app at https://developer.twitter.com/
2. Enable OAuth 2.0 in your app settings
3. Set the callback URL to `http://localhost:8000/callback`
4. Create a `.env` file in the root directory with the following variables:
   ```
   TWITTER_CLIENT_ID=your_client_id
   TWITTER_CLIENT_SECRET=your_client_secret
   TWITTER_REDIRECT_URI=http://localhost:8000/callback
   ```

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Visit `http://localhost:8000` to start
2. Click on the login link or visit `http://localhost:8000/login`
3. Authorize the application on Twitter
4. After successful authentication, you'll be redirected back to the application
5. To post a tweet, send a POST request to `http://localhost:8000/tweet` with the following JSON body:
   ```json
   {
       "text": "Your tweet text here"
   }
   ```

## API Endpoints

- `GET /`: Welcome message
- `GET /login`: Start OAuth2 authentication flow
- `GET /callback`: OAuth2 callback endpoint
- `POST /tweet`: Post a new tweet

## Security Notes

- This is a demo application and stores the OAuth2 handler in memory
- In a production environment, implement proper session management
- Store sensitive credentials securely
- Use HTTPS in production 
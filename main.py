from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
import tweepy
from config import get_settings
import uvicorn

app = FastAPI(title="Twitter OAuth2 Demo")
settings = get_settings()

# Store OAuth2 handler in memory (in production, use a proper session management)
oauth2_user_handler = None

@app.get("/")
async def root():
    print(f'***client ID: , {settings.TWITTER_CLIENT_ID}')
    print(f'***API Key: , {settings.TWITTER_API_KEY}')
    print(f'***API Secret: , {settings.TWITTER_API_SECRET}')
    print(f'***client secret: , {settings.TWITTER_CLIENT_SECRET}')
    return {"message": "Welcome to Twitter OAuth2 Demo. Go to /login to start"}

@app.get("/login")
async def login():
    global oauth2_user_handler
    
    # Initialize OAuth2UserHandler
    oauth2_user_handler = tweepy.OAuth2UserHandler(
        client_id=settings.TWITTER_CLIENT_ID,
        redirect_uri=settings.TWITTER_REDIRECT_URI,
        scope=settings.TWITTER_SCOPES,
        client_secret=settings.TWITTER_CLIENT_SECRET
    )
    
    # Get authorization URL
    auth_url = oauth2_user_handler.get_authorization_url()
    return RedirectResponse(url=auth_url)

@app.get("/callback")
async def callback(request: Request):
    global oauth2_user_handler
    
    if not oauth2_user_handler:
        raise HTTPException(status_code=400, detail="OAuth2 handler not initialized")
    
    # Get the full URL including query parameters
    callback_url = str(request.url)
    print(f"Callback URL: {callback_url}")  # Debug print
    
    try:
        # Fetch access token
        access_token = oauth2_user_handler.fetch_token(callback_url)
        print(f'Access token response: {access_token}')  # Debug print

        # Initialize Twitter client with OAuth 2.0
        client = tweepy.Client(
            consumer_key=settings.TWITTER_API_KEY,
            consumer_secret=settings.TWITTER_API_SECRET,
            access_token=access_token.get('access_token')
        )
        # consumer_key=settings.TWITTER_API_KEY,
        # consumer_secret=settings.TWITTER_API_SECRET,
        print(f'Client created with token: {access_token.get("access_token")}')  # Debug print
        
        # Get user information
        me = client.get_me()
        print(f'User info response: {me}')  # Debug print
        
        return {
            "message": "Successfully authenticated!",
            "user": me.data,
            "access_token": access_token
        }
    except Exception as e:
        print(f"Detailed error: {str(e)}")  # Debug print
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/tweet")
async def post_tweet(request: Request):
    global oauth2_user_handler
    
    if not oauth2_user_handler:
        raise HTTPException(status_code=400, detail="OAuth2 handler not initialized")
    
    try:
        # Get tweet text from request body
        # data = await request.json()
        # tweet_text = data.get("text")
        tweet_text = "Hello world, My first tweet"
        
        if not tweet_text:
            raise HTTPException(status_code=400, detail="Tweet text is required")
        
        # Initialize Twitter client
        client = tweepy.Client(
            consumer_key=settings.TWITTER_CLIENT_ID,
            consumer_secret=settings.TWITTER_CLIENT_SECRET,
            access_token=oauth2_user_handler.access_token
        )
        
        # Post tweet
        response = client.create_tweet(text=tweet_text)
        
        return {
            "message": "Tweet posted successfully!",
            "tweet_id": response.data["id"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 
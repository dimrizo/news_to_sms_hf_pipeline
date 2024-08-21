from twilio.rest import Client
import os

def send_sms_message_with_link(from_phone_number, to_phone_number, msg_body_txt, article_url, link_url):
    """
    Send an SMS message to a recipient who may want to use the information produced as an Insta Post.
    
    Parameters:
    - from_phone_number: Your Twilio phone number in E.164 format, e.g., '+12345678901'.
    - to_phone_number: The recipient's phone number in E.164 format, e.g., '+10987654321'.
    - msg_body_txt: This is either the title or the summary of the article, or a combination.
    - article_url: URL to actual article.
    - link_url: URL of the image produce by HF.
    """
    # Concatenate the body text and the link URL
    full_message = f"{msg_body_txt}, Article: {article_url}, Media: {link_url}"

    # Retrieve Twilio Account SID and Auth Token from environment variables
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=from_phone_number,  # Your Twilio phone number
        body=full_message,
        to=to_phone_number  # Recipient's phone number
    )

    print(f"Message SID: {message.sid}")

if __name__ == '__main__': # for testing purposes
    # Numbers for Twillio (E.164 format assumed)
    from_phone_number = os.getenv('FROM_NUMBER')
    to_phone_number = os.getenv('TO_NUMBER')

    msg_body_txt = "Here's your SMS message!"
    article_url = 'http://quotes.toscrape.com/author/Thomas-A-Edison/'
    link_url = "https://assets.fiba.basketball/image/upload/w_640,h_360,c_fill,g_auto/q_auto/f_auto/vtwdffyz6acd40w70rkw"  # The URL you want to include in the SMS

    send_sms_message_with_link(from_phone_number, to_phone_number, msg_body_txt, article_url,  link_url)

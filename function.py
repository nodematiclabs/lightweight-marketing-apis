import base64
import functions_framework

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

@functions_framework.http
def entrypoint(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': 'https://hello.example.com',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': 'https://hello.example.com',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }

    if request.path == "/newsletter-signup":
        # Newsletter subscription
        email = request.form.get('email')

        # Prepare data for SendGrid
        data = {
            "list_ids": [LIST_ID_HERE],
            "contacts": [
                {
                    "email": email
                }
            ]
        }

        try:
            # Create a SendGrid client
            sg = SendGridAPIClient('')
            response = sg.client.marketing.contacts.put(request_body=data)

            # Check the response
            if response.status_code == 202:
                return ("", 200, headers)
            else:
                return ("", 500, headers)

        except Exception:
                return ("", 500, headers)
    elif request.path == "/contact-us":
        # Contact form
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Prepare email content
        email_content = f"Name: {name}\n" \
                        f"Email: {email}\n" \
                        f"Message: {message}\n"

        # Construct the email
        email = Mail(
            from_email='marketing@example.com',
            to_emails='community@example.com',
            subject=f'New contact form request from {name}',
            plain_text_content=email_content
        )

        try:
            # Create a SendGrid client
            sg = SendGridAPIClient('')
            response = sg.send(email)
            # Check the response
            if response.status_code == 202:
                return ("", 200, headers)
            else:
                return ("", 500, headers)
        except Exception:
            return ("", 500, headers)
    else:
        return ('', 400, headers)
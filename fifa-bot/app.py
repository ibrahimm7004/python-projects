import os
from flask import Flask, request
import urllib2
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_sms():
    body = request.values.get('Body', '').strip()
    resp = MessagingResponse()

    response_message = get_wikipedia_info(body)

    resp.message(response_message)
    return str(resp)

def get_wikipedia_info(topic):
    try:
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        url = 'http://en.wikipedia.org/w/index.php?title={}&printable=yes'.format(topic)
        infile = opener.open(url)
        page = infile.read()

        # Process the 'page' variable to extract relevant information
        # You can use BeautifulSoup or regular expressions to extract the summary or any other information you need

        # For demonstration purposes, let's just return the entire HTML content as the response_message
        return page

    except urllib2.URLError as e:
        return "Error occurred while fetching information: {}".format(str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

from tweepy import *
import ConfigParser
import json
import pprint
import random
import string

def get_reply(text):
    """
    Returns a reply to the message text.
    """
    words = [w.strip(string.punctuation) for w in text.lower().split()]

    general_responses = ['try asking on Piazza!',
            'I recommend you go to office hours #NotMyProblem',
            'did you try googling that?',
            "I'm not sure! ask Maxim!",
            'Try re-reading the lecture slides',
            'This was covered in lecture',
            'Search Piazza!',
            'We will cover that in class later..',
        ]

    if 'autograder' in words:
        return random.choice(['uh oh.. I think we broke it..',
            "it's not a bug! just an undocumented feature!",
        ] + general_responses)
    elif 'extension' in words:
        return random.choice(['yeah! you can get an extension.. when hell freezes over!! #SorryNotSorry',
            ])
    elif 'office' in words and 'hours' in words:
        return random.choice(['current wait time: 2 weeks 5 days #subtweet #goaway',
            ] + general_responses)
    elif 'codelab' in words:
        return random.choice(['we have no clue what it means either!',
            ] + general_responses)
    elif 'style' in words:
        return random.choice(['ask Eva!!',
            "don't at me! I only got 5/10 for style!",
            "it's a magic number",
            "this code is unreadable!",
        ] + general_responses)
    else:
        return random.choice(general_responses)

def read_config():
    """
    Reads in the API_Keys from the configuration file, and returns as a dict
    """
    config = ConfigParser.ConfigParser()
    config.read('183help.cfg')
    return {key: val for (key, val) in config.items('API_Keys')}

class Listener183(StreamListener):

    def on_data(self, raw_data):
        data = json.loads(raw_data)
        # The new version of the Twitter streaming API initially responds
        # with a friends list, which tweepy doesn't handle correctly in this
        # version. So this is a hack to swallow that!
        if not 'friends' in data:
            return super(Listener183, self).on_data(raw_data)

    def on_status(self, status):
        # Make sure we don't reply to ourself!
        if status.author.id == self.api.me().id:
            return

        print 'status:'
        pprint.pprint(vars(status))

        # Create a response and reply
        response = '@{0} {1}'.format(status.author.screen_name, get_reply(status.text))
        pprint.pprint(vars(self.api.update_status(status=response, in_reply_to_status_id=status.id_str)))

    def on_event(self, status):
        print 'event:'
        pprint.pprint(vars(status))

if __name__ == '__main__':
    keys = read_config()
    auth = OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    l = Listener183(api=API(auth))
    stream = Stream(auth, l)

    try:
        stream.userstream()
    except KeyboardInterrupt:
        stream.disconnect()


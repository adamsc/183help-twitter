"""
Copyright 2014 Adam Schnitzer

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from tweepy import *
import ConfigParser
import json
import pprint
import random
import string

def get_reply(text):
    """
    Returns a reply to a given string.
    """
    # split into list of words in lowercase with punctuation removed
    words = [w.strip(string.punctuation) for w in text.lower().split()]

    # a list of responses which can be used for any question
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
        # returns a random element from the combination of the specific responses
        # for 'autograder', in addition to all general responses.
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
    Reads in the API_Keys from the configuration file, and returns as a dict.
    """
    config = ConfigParser.ConfigParser()
    config.read('183help.cfg')
    # this is a dictionary comprehension to return the config as key-value pairs.
    return {key: val for (key, val) in config.items('API_Keys')}

class Listener183(StreamListener):
    """
    This is a listener class which we specialize to call the get_reply function,
    and print out any data which is received.
    """
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
    # authenticate using the credentials in the config file
    keys = read_config()
    auth = OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    
    # create a stream using credentials, and begin the stream
    l = Listener183(api=API(auth))
    stream = Stream(auth, l)
    try:
        stream.userstream()
    except KeyboardInterrupt:
        stream.disconnect()


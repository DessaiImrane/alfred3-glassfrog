# encoding: utf-8

import sys
import pprint
from workflow import Workflow, ICON_WEB, web
import pprint


import os
API_KEY = os.environ['apikey']
PERSON_ID = os.environ['personid']
cache=os.environ['cache']

def get_web_data():
	url = "https://api.glassfrog.com/api/v3/people/%s/roles" % (PERSON_ID)
	headers = {'content-type': 'application/json', 'x-auth-token' : API_KEY}

	r = web.get(url, headers=headers)
	r.raise_for_status()
	result = r.json()
	roles = result['roles']
	return roles

def search_key_for_post(role):
     """Generate a string search key for a post"""
     elements = []
     #pprint.pprint(role)
     purpose = role['purpose']
     if role['purpose'] is None:
     	purpose = ''

     elements.append(purpose)  # title of post
     elements.append(role['name'])  # post tags
     return u' '.join(elements)

def main(wf):

# Get query from Alfred
 if len(wf.args):
	query = wf.args[0]
 else:
	query = None

 roles = wf.cached_data('glassrole', get_web_data, max_age=cache)

 if query:
	roles = wf.filter(query, roles, key=search_key_for_post,  min_score=20)

  
 # Loop through the returned posts and add an item for each to
 # the list of results for Alfred
 for role in roles:
     wf.add_item(title=role['name'],
                 subtitle=role['purpose'],
                 arg=str(role['id']),
                 valid=True,
                 icon=ICON_WEB)

 # Send the results to Alfred as XML
 wf.send_feedback()


if __name__ == u"__main__":
 wf = Workflow()
 sys.exit(wf.run(main))
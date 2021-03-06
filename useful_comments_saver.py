#!/usr/local/bin/python3
import argparse
import configparser

from api_objects import init_stepik, Comment
from google_utlis import load_links_from_google
from redmine_utils import get_or_create_issue, init_redmine

def get_path():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default='./')
    args = parser.parse_args()
    return (args.path)


SETTINGS_FILE_PATH = get_path() + 'settings.properties'

config = configparser.ConfigParser()
config.read(SETTINGS_FILE_PATH)

all_links = load_links_from_google(config['google']['sheet_id'], config['google']['sheet_range'])

if not init_stepik(config['stepik']['api_host'], config['stepik']['client_id'],
                   config['stepik']['client_secret']):
    raise RuntimeError('Cannot connect to stepik instance')

if not init_redmine(config['redmine']['api_host'], config['redmine']['api_key'], config['redmine']['project']):
    raise RuntimeError('Cannot connect to redmine server')

created = 0
for link in all_links:
    comment = Comment.retrieve(link=link)
    c, issue = get_or_create_issue(comment)
    created += int(c)

print('{} were created'.format(created))

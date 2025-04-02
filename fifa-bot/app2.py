import os
from flask import Flask, request
import requests
from dateutil import parser, tz
from twilio.twiml.messaging_response import MessagingResponse

urls = {'group': 'https://worldcup.sfg.io/teams/group_results',
'country': 'https://worldcup.sfg.io/matches/country?fifa_code=',
'today': 'https://worldcup.sfg.io/matches/today',
'tomorrow': 'https://worldcup.sfg.io/matches/tomorrow'
}


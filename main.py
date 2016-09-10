#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.api import mail, app_identity
from models import User, Game


class SendReminderEmail(webapp2.RequestHandler):
    def get(self):
        """Send a reminder email to each User with an email about
        unfinished games. Called periodically using a cron job"""
        app_id = app_identity.get_application_id()
        # TODO: Maybe make this a projection query to only pull back player1 & 2
        games = Game.query(Game.game_over != True)
        users = User.query(User.email != None)
        for game in games:
            users = [game.player1, game.player2]

            for user_key in users:
                user = user_key.get()

                subject = 'You have an unfinished game'
                body = 'Hello {}, you have an unfinished game of Connect 4'.format(user.name)
                # This will send test emails, the arguments to send_mail are:
                # from, to, subject, body
                mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
                               user.email,
                               subject,
                               body)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello everyone!')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/crons/send_reminder', SendReminderEmail),
], debug=True)

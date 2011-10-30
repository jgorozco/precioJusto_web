from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from frwk.getBid import getBid
from frwk.uploadBid import uploadBid
from frwk.getScore import getScore
from frwk.setBidPrize import setBidPrize


class MainPage(webapp.RequestHandler):
    
    
    def get(self):
        user = users.get_current_user()

        if user:
            self.response.out.write(
                'Hello %s <a href="%s">Sign out</a><br>Is administrator: %s' % 
                (user.nickname(), users.create_logout_url("/"), users.is_current_user_admin())
            )
        else:
            self.redirect(users.create_login_url(self.request.uri))


application = webapp.WSGIApplication([('/', MainPage),
                                      ('/getBids', getBid),#TODO
                                      ('/setBidPrize', setBidPrize),
                                      ('/uploadBid', uploadBid),
                                      ('/getScore', getScore)], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()

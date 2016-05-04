from . import BaseHandler

"""Handler for informational pages (i.e. just blocks of text)"""

class AboutHandler(BaseHandler):
    def get(self):
        referer = self.request.headers.get("Referer")
        print(referer)

        text = [
        """ClassRank is an application that uses collaborative filtering to help
        personalize class recommendations. Collaborative filtering is a machine
        learning algorithm that recognizes users like you. After finding those
        similar users, it uses a weighted average algorithm. The results of
        this algorithm are then used to select recommendations. Similar users
        can be found in a variety of ways, generally the algorithm uses a
        variant of the distance formula.""",

        """Once the system finds personalized ratings, it can present them to
        the user in a variety of ways. It can use them to recommend courses,
        professors, or schedules. This provides an incentive for students to
        rate professors. As the students provide truthful ratings, the
        analytics they receive becomes more accurate. As more students join,
        the accuracy of the system increases because there are more users to
        compare to.""",

        """The system is then able to solve a common problem: that students are
        different and what is easy for me may not be easy for you. Our team
        brings experience in machine learning, which encompasses collaborative
        filtering. We also bring experience in web development and front-end
        design. This means that we have the technical skills to create the
        complex analytic engine and the web design skills to make the
        application useful.""",

        """We believe that we can create a successful application that
        collects, analyzes, and presents user data. We think that we can do
        this while developing with best practices. The end result should be a
        useful, extensible application with long-term applicability."""
        ]

        # If a '/' is the last character in the referer (i.e. call from /home)
        if referer is None or len(referer) == referer.rfind('/') + 1:
            # Write out without a navbar
            self.render("info.html", subtitle="About", paragraphs=text)
        else:
            # otherwise, print it out with the navbar and such
            self.render("info_with_navbar.html", paragraphs=text)

class PrivacyHandler(BaseHandler):
    def get(self):
        referer = self.request.headers.get("Referer")
        text = [
        """ClassRank takes privacy as an utmost concern. Your ratings, email
        addresses, password, and all personal information are kept secure, and
        are completely inaccessible from any parties, inside and out. Your
        information is in safe hands"""
        ]

        # If a '/' is the last character in the referer (i.e. call from /home)
        if referer is None or len(referer) == referer.rfind('/') + 1:
            # Write out without a navbar
            self.render("info.html", subtitle="Privacy", paragraphs=text)
        else:
            # otherwise, print it out with the navbar and such
            self.render("info_with_navbar.html", paragraphs=text)

class SecurityHandler(BaseHandler):
    def get(self):
        referer = self.request.headers.get("Referer")
        text = [
        """ClassRank takes privacy as an utmost concern. Your ratings, email
        addresses, password, and all personal information are kept secure, and
        are completely inaccessible from any parties, inside and out. Your
        information is in safe hands."""
        ]

        # If a '/' is the last character in the referer (i.e. call from /home)
        if referer is None or len(referer) == referer.rfind('/') + 1:
            # Write out without a navbar
            self.render("info.html", subtitle="Security", paragraphs=text)
        else:
            # otherwise, print it out with the navbar and such
            self.render("info_with_navbar.html", paragraphs=text)

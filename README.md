#SocialDigger
A CRM analytics tool for your social media.

Backend: Python web framework "Flask"

Frontend: Basic bootstrap template, will integrate sb2-admin template soon.

This is a Flask app which intends to act as a customer relationship management(CRM) tool for companies to analyze their current followers on Twitter using machine learning algorithms to create user frequency profiles and by classification then identify new potential followers on social media, or continiously analyzing opinion and sentiment shift from current followers.

Flask is written in Python and the backend is migrated to SQLite. Bootstrap 3.2.0 is utilized for the frontend design(forked from flask-bootstrap repository - thank you!).

To fork the app, do initialize a virtual environment with virtualenv and clone into it. The dependencies are described in requirements.txt, but do also install bootstrap 3.2.0.
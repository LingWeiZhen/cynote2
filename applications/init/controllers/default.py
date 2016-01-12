from datetime import date
import time

password_age = 90 # password expiry = 90 days
login_expiry = 24 # login expiry = 24 hours
version = '2.0'
copyright = {
            'year': '2016-%s' % str(date.today().year),
            'director': 'Maurice Ling',
            'license': '''CyNote 2 is a proprietary software.'''
            }

cynote_header = '''Welcome to CyNote 2 - A web-enabled notebook compliant 
with general research record-keeping standard (US FDA 21 CFR Part 11)'''
    
cynote_dependencies = [#'biopython==1.56',
                       #'pil==1.1.6'
                      ]

if not session.has_key('login_count'): 
    session.login_count = 0

def check_login(session=session):
    if session.login_time == None: 
        session.login_time = 0
    if session.username == None:
        #session.login_time + login_expiry * 3600 < int(time.time()): 
        redirect(URL(r=request, c='account', f='log_in'))
    else: 
        return session.username

def index():
    response.flash = cynote_header
    name = check_login()
    #if password_aging(session.username) == True:
    #    session.pwdaged = True
    #    redirect(URL(r=request, c='account', f='change_password'))
    return dict(tab_list=session.installed_plugins, name=name, 
                version=version, copyright=copyright,
                message=T('CyNote Main Menu'))

# from ez_setup import use_setuptools
# use_setuptools()
# from setuptools.command.easy_install import main

# session.installed_plugins[('default', 'bioinformatics')] = 'Bioinformatics Tools'
# session.installed_plugins[('default', 'statistics')] = 'Statistical Analysis'
# session.installed_plugins[('default', 'adhocDB')] = 'Ad hoc Research Database'

# tabs = session.installed_plugins
# try: session['dependencies']
# except KeyError: session['dependencies'] = 'NOT DONE'
# if session['dependencies'] != 'DONE':
	# for dependency in cynote_dependencies:
		# try: 
			# main([dependency])
		# except KeyError: 
			# print dependency + ' installation error'
		# except: 
			# print dependency + ' generic error (please inform Maurice Ling)'
		# session['dependencies'] = 'DONE'
			
'''
def password_aging(username, password_age=password_age):
    current_time = int(time.time())
    last_password_change = userdb(userdb.user.username == username) \
                           .select(userdb.user.aging)[0]['aging']
    # print current_time, last_password_change
    if last_password_change == None or \
    last_password_change + (password_age * 24 * 3600) < current_time:
        db.user_event.insert(event='Password aged > 90 days. %s' % \
            session.username, 
            user='system')
        return True
    else: 
        return False'''




@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

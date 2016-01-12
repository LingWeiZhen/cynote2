from time import time
from hashlib import sha512 as h
from random import random


def new_account():
    '''
    Creating a new user account.
    CyNote 2 ready.
    '''
    if user(user.user.username > 0).count() == 0: 
        authorized = True
    else: 
        authorized = False
    form = FORM(TABLE(
                TR('Actual Name:', 
                   INPUT(_name='actualname',
                         requires=IS_NOT_EMPTY()
                        )),
                TR('User Name:', 
                   INPUT(_name='username',
                         requires=IS_NOT_EMPTY()
                        )),
                TR('Email Address:', 
                   INPUT(_name='email',
                         requires=IS_EMAIL(error_message='invalid email!')
                        )),
                TR('Password:', 
                   INPUT(_name='password',
                         requires=[IS_NOT_EMPTY()]
                        )),
                TR('Personal Encryption Key:', 
                   INPUT(_name='encryptkey',
                         requires=[IS_NOT_EMPTY()]
                        )),
                TR('', INPUT(_type='submit', _value='login')))) 
    if form.accepts(request.vars, session):
        user.user.insert(username=form.vars.username,
                           actualname=form.vars.actualname,
                           email=form.vars.email,
                           password=h(form.vars.password).hexdigest(),
                           encryptkey=h(form.vars.encryptkey).hexdigest(),
                           aging=time(),
                           authorized=authorized)
        bb.tape.insert(user='system',
                       entrycode='new_user_account',
                       refcode='',
                       event='User Name = %s. Actual Name = %s. Email = %s.' % \
                           (form.vars.username, 
                            form.vars.actualname, 
                            form.vars.email))
        redirect(URL(r=request, f='log_in'))
    return dict(form=form)


def log_in():
    '''
    Function for user to log in.
    Compares the user login, password, and personal encryption key with 
    user.user table
    If login is successful, the username is stored in session.username
    for further use. If login is not successful, session.username = None
    CyNote 2 ready.
    '''
    form = FORM(TABLE(
                TR('User Name:', 
                   INPUT(_name='username',
                         requires=IS_NOT_EMPTY()
                        )),
                TR('Password:', 
                   INPUT(_name='password', _type='password',
                         requires=[IS_NOT_EMPTY()]
                        )),
                TR('Personal Encryption Key:', 
                   INPUT(_name='encryptkey', _type='password',
                         requires=[IS_NOT_EMPTY()]
                        )),
                TR('', INPUT(_type='submit', _value='login')))) 
    if form.accepts(request.vars, session):
        if user(user.user.username == form.vars.username) \
            (user.user.password == h(form.vars.password).hexdigest()) \
            (user.user.encryptkey == h(form.vars.encryptkey).hexdigest()) \
            (user.user.authorized == True).count():
            session.username = form.vars.username
            session.encryptkey = form.vars.encryptkey
            session.ID = str(1000000000 * random())
            bb.tape.insert(user=session.username,
                           entrycode='user_login_success',
                           refcode=session.ID,
                           event='User Name = %s. Session ID = %s. Password hash = %s. Encryptkey hash = %s' % \
                           (session.username, 
                            session.ID, 
                            h(form.vars.password).hexdigest(),
                            h(form.vars.encryptkey).hexdigest()))
            session.login_count = 1
            redirect(URL(r=request, f='logged'))
        else:
            bb.tape.insert(user='system',
                           entrycode='user_login_fail',
                           refcode='',
                           event='User name used = %s. Given password hash = %s. Given encryptkey hash = %s. Login count = %s' % \
                           (form.vars.username, 
                            h(form.vars.password).hexdigest(),
                            h(form.vars.encryptkey).hexdigest(),
                           str(session.login_count)))
            session.username = None
            response.flash = 'invalid username/password'
            if session.login_count == None: session.login_count = 0
            session.login_count = session.login_count + 1
    return dict(form=form)


def logged():
    """redirection when login is successful"""
    session.login_time = time()
    return dict(name=session.username)


def log_out():
    """Set session.username to None when logged out"""
    db.user_event.insert(event='Logout. %s' % \
                         session.username, 
                         user='system')
    session.username = None
    return dict(name=session.username)

user=SQLDB("sqlite://users.db")

#the username table
user.define_table('user',
                  SQLField('username', 'string', unique=True),
                  SQLField('actualname', 'string'),
                  SQLField('email', 'string'),
                  SQLField('password', 'string'),
                  SQLField('encryptkey', 'string'),
                  SQLField('aging', 'integer'),
                  SQLField('authorized', 'boolean'))

user.user.username.requires = IS_NOT_EMPTY()
user.user.username.requires = IS_NOT_IN_DB(user, 'user.username')

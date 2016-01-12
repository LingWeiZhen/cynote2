import datetime; now=datetime.datetime.utcnow()
import uuid

bb = SQLDB('sqlite://blackbox.db')

bb.define_table('tape',
                SQLField('user'),
                SQLField('entrycode'),
                SQLField('refcode'),
                SQLField('event', 'text'),
                SQLField('modified_on', 'datetime', default=now))

bb.define_table('entry_hash',
                SQLField('eid'),
                SQLField('edatetime'),
                SQLField('etitle', 'text'),
                SQLField('hashed', 'datetime', default=now),
                SQLField('ehash', 'text'))
                
bb.define_table('comment_hash',
                SQLField('cid'),
                SQLField('cdatetime'),
                SQLField('eid'),
                SQLField('hashed', 'datetime', default=now),
                SQLField('chash', 'text'))

bb.define_table('track_entry_hash',
                SQLField('eid'),
                SQLField('edatetime'),
                SQLField('etitle', 'text'),
                SQLField('hashed', 'datetime', default=now),
                SQLField('ehash', 'text'))
                
bb.define_table('track_comment_hash',
                SQLField('cid'),
                SQLField('cdatetime'),
                SQLField('eid'),
                SQLField('hashed', 'datetime', default=now),
                SQLField('chash', 'text'))
                
bb.define_table('file_hash',
                SQLField('filename'),
                SQLField('hashed', 'datetime', default=now),
                SQLField('fhash', 'text'))

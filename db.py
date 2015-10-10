import rethinkdb as r

def get_conn ():
    return r.connect(host='127.0.0.1', port=28015, db='monitorSitesBot')

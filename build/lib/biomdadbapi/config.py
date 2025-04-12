import os, sys, argparse
from configparser import ConfigParser, NoOptionError, NoSectionError

def add_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', dest='database', required=True,
                        help='The path of BioMDA database')
    parser.add_argument('-o', '--host', dest='host', required=False,
                        help='The host of http://[host]:port, defualt 127.0.0.1',
                        default='127.0.0.1')
    parser.add_argument('-p', '--port', dest='port', required=False,
                        help='The port of http://host:[port], defualt 8000',
                        default='8000')
    args=parser.parse_args()
    db = args.database
    host = args.host
    port = args.port
    if not os.path.exists(db):
        print('The path of BioMDA database is not exist.')
        sys.exit()
    else:
        conf = ConfigParser()
        dir = os.path.dirname(os.path.abspath(__file__))
        cfg_file = os.path.join(dir, 'BioMDA-DB.cfg')
        cfg_open = open(cfg_file, 'w')
        conf.add_section('defualt')
        conf.set("defualt", "database", db)
        conf.set("defualt", "host", host)
        conf.set("defualt", "port", port)
        conf.write(cfg_open)
        cfg_open.close()
        print('Add options for section[defualt] in {cfg}'.format(cfg = cfg_file))
        print('Add database: {db}'.format(db = db))
        print('Add database: {host}'.format(host = host))
        print('Add database: {port}'.format(port = port))

def get_config():
    conf = ConfigParser()
    dir = os.path.dirname(os.path.abspath(__file__))
    conf.read(os.path.join(dir, 'BioMDA-DB.cfg'))
    try:
        db = conf.get('defualt', 'database')
    except NoSectionError:
        print('******')
        print('Execute biomdadb-add-config to add options for defualt config.')
        print('biomdadb-add-config -h')
        print('******')
        sys.exit()
    except NoOptionError:
        db = ''
    host = conf.get('defualt', 'host')
    port = conf.get('defualt', 'port')
    opt = {'db': db, 'host': host, 'port': port}
    return opt

def show_config():
    dir = os.path.dirname(os.path.abspath(__file__))
    cfg_file = os.path.join(dir, 'BioMDA-DB.cfg')
    with open(cfg_file, 'r') as f:
        print(f.read())
    print('******')
    print('Execute biomdadb-add-config to add options for defualt config.')
    print('biomdadb-add-config -h')
    print('******')
# -*- coding: utf-8 -*-
from base64 import b64encode
import flask
import requests
import sys
import os
import subprocess
import logging
from path import path
from celery import Celery
from celery.signals import setup_logging
from tempfile import NamedTemporaryFile as NamedTempFile
from tempfile import TemporaryFile
#from harvest import appcontext

import utils


celery = Celery()
celery.config_from_object('celeryconfig')

@setup_logging.connect
def configure_worker(sender=None, **extra):
    from utils import set_up_logging
    set_up_logging()

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def es_search(text, fields=None, page=1, per_page=20):
    es_url = flask.current_app.config['PUBDOCS_ES_URL']
    search_data = {
        "fields": ["title"],
        "query": {
            "query_string": {"query": text},
        },
        "highlight": {
            "fields": {"file": {}},
        },
    }
    search_url = es_url + '/_search'
    search_url += '?from=%d&size=%d' % ((page - 1) * per_page, per_page)
    if fields is not None:
        search_url += '&fields=' + ','.join(fields)
    search_resp = requests.get(search_url, data=flask.json.dumps(search_data))
    assert search_resp.status_code == 200, repr(search_resp)
    return search_resp.json


search_pages = flask.Blueprint('search', __name__, template_folder='templates')

def appcontext(func):
    def wrapper(*args, **kwargs):
        import manage
        app = manage.create_app()
        with app.app_context():
            return func(*args, **kwargs)
    return wrapper

@celery.task
@appcontext
def index(file_path):
    """ Index a file from the repositoy. """
    from harvest import build_fs_path
    es_url = flask.current_app.config['PUBDOCS_ES_URL']
    repo = flask.current_app.config['PUBDOCS_FILE_REPO'] / ''

    (section, year, name) = file_path.replace(repo, "").split('/')
    fs_path = build_fs_path(file_path)
    with NamedTempFile(mode='w+b', delete=True) as temp:
        try:
            subprocess.check_call('pdftotext %s %s' %(fs_path, temp.name),
                                  shell=True)
        except Exception as exp:
            log.critical(exp)

        clean(temp.name, False)
        index_data = {
            'file': b64encode(temp.read()),
            'path': file_path,
            'year': int(year),
            'section': int(section[3:]),
        }
        log.info('Indexing %s' %file_path)
        index_resp = requests.post(es_url + '/mof/attachment/' + name,
                                   data=flask.json.dumps(index_data))
        assert index_resp.status_code in [200, 201], repr(index_resp)
        if index_resp.status_code == 200:
            log.info('Skipping. Already indexed!')

def replace(match, text, debug=False):
    changes_log_path = path(flask.current_app.config['PUBDOCS_CHANGES_LOG'])
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
    try:
        bad = match.group(0)
        good = utils.chars_mapping[bad]
        old = (text[match.start()-10:match.start()] +
               bcolors.FAIL +
               bad +
               bcolors.ENDC +
               text[match.end():match.end()+10]
              )
        new = (text[match.start()-10:match.start()] +
               bcolors.OKGREEN +
               good +
               bcolors.ENDC +
               text[match.end():match.end()+10]
              )
        text = text.replace(bad, good)
        message = '%s\n%s\n' %(old, new)
        if debug:
            log.info(message)
        else:
            with changes_log_path.open('a') as clog:
                clog.write('------------%s------------\n' %bad)
                sys.stdout.write(message)
    except Exception as exp:
        if debug:
            pass
            #import pdb; pdb.set_trace()

import re
pat3 = re.compile(r'([^\x00-\x7F][^\x00-\x7F][^\x00-\x7F])')
pat2 = re.compile(r'([^\x00-\x7F][^\x00-\x7F])')
def clean(file_path, debug):
    """ Index a file from the repositoy. """
    if not debug == 'debug':
        debug = False
    fs_path = path(file_path)
    cursor = 0
    total = fs_path.getsize()

    with fs_path.open('r') as data:
        with NamedTempFile(mode='a', delete=False) as cleaned:
            text = data.read()
            for match in pat3.finditer(text):
                replace(match, text)
            for match in pat2.finditer(text):
                replace(match, text)
    with open(cleaned.name, 'rb') as f:
        with fs_path.open('wb') as origin:
            origin.write(text)


@search_pages.route('/')
def search():
    args = flask.request.args

    q = args.get('q')
    if q:
        page = args.get('page', 1, type=int)
        results = es_search(q, ['year', 'section', 'path'], page=page)
        next_url = flask.url_for('.search', page=page + 1, q=q)

    else:
        results = None
        next_url = None

    return flask.render_template('search.html', **{
        'results': results,
        'next_url': next_url,
    })


def register_commands(manager):

    @manager.command
    def flush():
        """ Flush the elasticsearch index """
        es_url = flask.current_app.config['PUBDOCS_ES_URL']

        del_resp = requests.delete(es_url + '/mof')
        assert del_resp.status_code in [200, 404], repr(del_resp)

        index_config = {
            "settings": {
                "index": {"number_of_shards": 1,
                          "number_of_replicas": 0},
            },
        }
        create_resp = requests.put(es_url + '/mof',
                                   data=flask.json.dumps(index_config))
        assert create_resp.status_code == 200, repr(create_resp)

        attachment_config = {
            "document": {
                "properties": {
                    "file": {
                        "type": "attachment",
                        "fields": {
                            "title": {"store": "yes"},
                            "file": {"store": "yes",
                                     "term_vector": "with_positions_offsets"},
                        },
                    },
                },
            },
        }
        attach_resp = requests.put(es_url + '/mof/attachment/_mapping',
                                   data=flask.json.dumps(attachment_config))
        assert attach_resp.status_code == 200, repr(attach_resp)

    @manager.command
    def search(text):
        """ Search the index. """
        print flask.json.dumps(es_search(text), indent=2)

    @manager.command
    def index_section(section, debug):
        """ Bulk index pdfs from specified section. """
        import os
        import subprocess
        changes_log_path = path(flask.current_app.config['PUBDOCS_CHANGES_LOG'])
        if changes_log_path.exists():
            os.remove(changes_log_path)
        section_path = flask.current_app.config['PUBDOCS_FILE_REPO'] / section
        args = 'find %s -name "*.pdf" | wc -l' % (str(section_path))
        total = int(subprocess.check_output(args, shell=True))
        indexed = 0
        for year in os.listdir(section_path):
            year_path = section_path / year
            for doc_path in year_path.files():
                name = doc_path.name
                index.delay(doc_path)
                #index(doc_path)
                indexed += 1
                sys.stdout.write("\r%i/%i" % (indexed, total))
                sys.stdout.flush()

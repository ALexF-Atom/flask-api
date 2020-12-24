from flask import render_template, jsonify, request, make_response

from . import index
from redisconfig import RedisConfig as RCG


@index.route('/')
def start_page():
    context = {}
    context['message'] = 'Start App'
    context['title'] = 'Index'
    return render_template('index.html', **context)


@index.route('/api/0.1/', methods=['GET'])
def api_page():
    s = request.query_string.decode().upper()
    print(s)
    if s.isdigit() or not s:
        return make_response(jsonify({'error': 'Nothing'}), 403)

    from app import RedisClient
    with RedisClient(db=RCG.DB_DATA) as r:
        d = {key.decode(): r.get(key).decode() for key in r.keys(f'{s}*')}

    return jsonify(d)


@index.route('/api/0.1/company/', methods=['GET'])
def api_company():
    s = request.query_string.decode().upper()

    if s.isdigit() or not s:
        return make_response(jsonify({'error': 'Nothing'}), 403)

    from app.task import get_company
    return jsonify(get_company(s))

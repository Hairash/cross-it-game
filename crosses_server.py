import random

from flask import Flask, jsonify, redirect, request, render_template, url_for

app = Flask(__name__)

FIELD_SIZE = 10



def generate_field(n):
    return [[-1] * n for _ in range(n)]


def make_move(field, x0, y0, player):
    coords_to_fill_list = [
        (x0, y0),
        (x0 - 1, y0),
        (x0 + 1, y0),
        (x0, y0 - 1),
        (x0, y0 + 1),
    ]
    for x, y in coords_to_fill_list:
        if x < 0 or y < 0 or x >= FIELD_SIZE or y >= FIELD_SIZE:
            raise Exception('Cannot make move out of the field')
        if field[x][y] != -1:
            raise Exception('Cell is already occupied')

    for x, y in coords_to_fill_list:
        field[x][y] = player


app_data = {
    'field': generate_field(FIELD_SIZE),
    'current_player': 0,
    'players_num': 0,
}


@app.route('/', methods=['GET'])
def home():
    return render_template('crosses_client.html', field=app_data['field'], size=FIELD_SIZE)


@app.route('/field', methods=['GET'])
def get_field():
    return jsonify(app_data['field'])


@app.route('/move', methods=['POST'])
def handle_move():
    data = request.json
    print(data)
    player = app_data['current_player']
    if int(data['player']) != player:
        return jsonify({'message': 'Not your turn!'})

    x, y = map(int, data['coords'])
    print(x, y)
    try:
        make_move(app_data['field'], x, y, player)
    except Exception as e:
        print(e)
        return jsonify({'message': str(e)})
    app_data['current_player'] = (player + 1) % 2
    return jsonify({'message': 'Move done'})


@app.route('/player', methods=['GET'])
def get_player():
    player = app_data['players_num']
    app_data['players_num'] += 1
    return str(player)


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

FIELD_SIZE = 10


def generate_field(n):
    return [[-1] * n for _ in range(n)]


app_data = {
    'field': generate_field(FIELD_SIZE),
    'current_player': 0,
}


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


@app.route('/', methods=['GET'])
def home():
    return render_template('crosses_client.html', field=app_data['field'], size=FIELD_SIZE)


@app.route('/game', methods=['GET'])
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
    try:
        make_move(app_data['field'], x, y, player)
    except Exception as e:
        print(e)
        return jsonify({'message': str(e)})

    app_data['current_player'] = (player + 1) % 2
    return jsonify({'message': 'Move done'})


@app.route('/new_game', methods=['POST'])
def start_new_game():
    app_data['field'] = generate_field(FIELD_SIZE)
    app_data['current_player'] = 0
    return jsonify({'message': 'New game started'})


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, render_template, request
from champions_data import CHAMPIONS

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200


@app.route('/api/info')
def info():
    return jsonify({
        'app': 'Bestiaire LoL - CI/CD Test',
        'version': '1.0.0',
        'total_champions': len(CHAMPIONS)
    })


@app.route('/api/champions')
def get_champions():
    """Retourne tous les champions avec filtres optionnels"""
    lane = request.args.get('lane')
    race = request.args.get('race')
    year = request.args.get('year', type=int)
    energy = request.args.get('energy')
    range_type = request.args.get('range')

    filtered = CHAMPIONS

    if lane:
        filtered = [c for c in filtered if lane in c['lane']]
    if race:
        filtered = [c for c in filtered if race.lower() in c['race'].lower()]
    if year:
        filtered = [c for c in filtered if c['year'] == year]
    if energy:
        filtered = [c for c in filtered if energy.lower() in c['energy'].lower()]
    if range_type:
        filtered = [c for c in filtered if range_type.lower() in c['range'].lower()]

    return jsonify(filtered)


@app.route('/api/champions/<name>')
def get_champion(name):
    """Retourne un champion par son nom"""
    champion = next(
        (c for c in CHAMPIONS if c['name'].lower() == name.lower()),
        None
    )
    if champion:
        return jsonify(champion)
    return jsonify({'error': 'Champion non trouvé'}), 404


@app.route('/api/stats')
def get_stats():
    """Retourne des statistiques sur les champions"""
    lanes = {}
    races = {}
    years = {}
    energies = {}
    ranges = {'Corps à corps': 0, 'Distance': 0}

    for c in CHAMPIONS:
        for lane in c['lane']:
            lanes[lane] = lanes.get(lane, 0) + 1
        races[c['race']] = races.get(c['race'], 0) + 1
        years[c['year']] = years.get(c['year'], 0) + 1
        energies[c['energy']] = energies.get(c['energy'], 0) + 1
        ranges[c['range']] = ranges.get(c['range'], 0) + 1

    return jsonify({
        'total': len(CHAMPIONS),
        'by_lane': lanes,
        'by_race': dict(sorted(races.items(), key=lambda x: x[1], reverse=True)[:10]),
        'by_year': dict(sorted(years.items())),
        'by_energy': energies,
        'by_range': ranges
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

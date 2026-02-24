import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'


def test_info(client):
    response = client.get('/api/info')
    assert response.status_code == 200
    data = response.get_json()
    assert data['app'] == 'Bestiaire LoL - CI/CD Test'
    assert data['version'] == '1.0.0'
    assert 'total_champions' in data


def test_get_all_champions(client):
    response = client.get('/api/champions')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 100  # Plus de 100 champions


def test_get_champion_by_name(client):
    response = client.get('/api/champions/Ahri')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Ahri'
    assert data['race'] == 'Vastaya'
    assert data['energy'] == 'Mana'


def test_get_champion_not_found(client):
    response = client.get('/api/champions/FakeChampion')
    assert response.status_code == 404


def test_filter_by_lane(client):
    response = client.get('/api/champions?lane=ADC')
    assert response.status_code == 200
    data = response.get_json()
    for champion in data:
        assert 'ADC' in champion['lane']


def test_filter_by_range(client):
    response = client.get('/api/champions?range=distance')
    assert response.status_code == 200
    data = response.get_json()
    for champion in data:
        assert 'Distance' in champion['range']


def test_stats(client):
    response = client.get('/api/stats')
    assert response.status_code == 200
    data = response.get_json()
    assert 'total' in data
    assert 'by_lane' in data
    assert 'by_race' in data
    assert 'by_year' in data
    assert 'by_energy' in data
    assert 'by_range' in data

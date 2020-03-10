import os
import tempfile

import pytest

from songboxproject import songbox


@pytest.fixture
def client():
    db_fd, songbox.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True

    with songbox.app.test_client() as client:
        with songbox.app.app_context():
            songbox.init_db()
        yield client

    os.close(db_fd)
    os.unlink(songbox.app.config['DATABASE'])

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data



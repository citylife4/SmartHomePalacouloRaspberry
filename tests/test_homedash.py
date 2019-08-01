import os
import tempfile

import pytest

from .. import homedash


@pytest.fixture
def client():
    db_fd, homedash.app.config['DATABASE'] = tempfile.mkstemp()
    homedash.app.config['TESTING'] = True

    with homedash.app.test_client() as client:
        with homedash.app.app_context():
            homedash.db.init_app()
        yield client

    os.close(db_fd)
    os.unlink(homedash.app.config['DATABASE'])
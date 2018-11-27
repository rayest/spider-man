import os

from betamax import Betamax
from betamax.fixtures.unittest import BetamaxTestCase

CASSETTES_DIR = 'tests/cassettes'


class BaseTest(BetamaxTestCase):
    with Betamax.configure() as config:
        os.makedirs(CASSETTES_DIR) if not os.path.exists(CASSETTES_DIR) else None
        config.cassette_library_dir = CASSETTES_DIR
        config.preserve_exact_body_bytes = True

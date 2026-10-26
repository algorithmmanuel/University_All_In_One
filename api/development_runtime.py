"""Local development guards; imports do not connect to a database."""
from urllib.parse import parse_qsl, urlsplit
from uuid import uuid4


def validate_development_database(value):
    """Reject beta targets and driver options that could redirect connections."""
    try:
        url = urlsplit(value)
        valid = (
            url.scheme == 'postgresql+psycopg'
            and url.hostname == '127.0.0.1' and url.port == 5435
            and url.path == '/educyber_dev' and url.username == 'educyber_dev'
            and bool(url.password) and not url.fragment
            and parse_qsl(url.query, keep_blank_values=True) in (
                [], [('connect_timeout', '5')]
            )
            and not any(character.isspace() for character in value)
        )
    except (TypeError, ValueError):
        valid = False
    if not valid:
        raise ValueError('Refusing to run outside the dedicated development database')


def add_development_health(app, environment):
    """Provide non-secret process identity only in explicitly isolated local mode."""
    if environment.get('EDUCYBER_LOCAL_DEVELOPMENT') != 'enabled':
        return
    if environment.get('EDUCYBER_ENV') != 'development':
        raise ValueError('Local runtime identity requires development mode')
    validate_development_database(environment.get('DATABASE_URL', ''))
    instance_id = uuid4().hex

    @app.get('/health/development', include_in_schema=False)
    def development_health():
        return {'environment': 'isolated-development', 'instance_id': instance_id}

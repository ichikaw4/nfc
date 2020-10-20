import click
from flask.cli import with_appcontext
from .models import User, Purpose, Record, PurposeMaster
from .database import db


@click.command('seed')
@click.argument('arg')
@with_appcontext
def seed(arg):
    if arg == 'purpose':
        seed_purpose_master()


def seed_purpose_master():
    purpose_master = [
        PurposeMaster(
            '研究活動', 'seeder'),
        PurposeMaster(
            '管理業務', 'seeder'),
        PurposeMaster(
            'TA業務', 'seeder'),
        PurposeMaster(
            '事務作業', 'seeder')]

    try:
        db.session.add_all(purpose_master)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


def register_command(app):
    app.cli.add_command(seed)

import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Player,
    Score,
    Map,
    TopRating,
    Base,
    )

#DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

from pyramid.httpexceptions import (
HTTPFound,
HTTPNotFound,
)

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        pl1 = Player(id=1, name='elf80lvl')
        DBSession.add(pl1)

	pl2 = Player(id=2, name='ffssa')
	DBSession.add(pl2)

	pl3 = Player(id=3, name='pfffff')
	DBSession.add(pl3)

	pl4 = Player(id=4, name='nickname')
	DBSession.add(pl4)

	pl5 = Player(id=5, name='cosmicPlayer')	
        DBSession.add(pl5)

	map1 = Map(id=1, name='Khalkhin-Gol')
	DBSession.add(map1)

	map2 = Map(id=2, name='Sevastopol')
	DBSession.add(map2)

	map3 = Map(id=6, name='Stalingrad')
	DBSession.add(map3)

	rate1 = TopRating(id=1, map_id = 1, first_user_name=pl5.name, second_user_name=pl1.name, third_user_name=pl3.name)
        DBSession.add(rate1)

	topRating2 = TopRating(id=2, map_id = 1, first_user_name=pl5.name, second_user_name=pl1.name, third_user_name=pl3.name)
	DBSession.add(topRating2)

	DBSession.commit
	

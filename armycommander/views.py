from pyramid.response import Response
from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Player,
    Score,
    Map,
    TopRating,
    AccessGroups,
    )

from pyramid.httpexceptions import (
HTTPFound,
HTTPNotFound,
)

from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from pyramid.security import (
remember,
forget,
)

from .security import USERS

@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
   if request.authenticated_userid == "admino":
    	return {'username': request.authenticated_userid, 'project': 'ArmyCommander'}
   return {'project': 'ArmyCommander'}

@view_config(route_name='map', renderer='templates/map.jinja2')
def maps(request):
    if request.authenticated_userid == "admino":
    	return {'username': request.authenticated_userid, 'project': 'ArmyCommander'}
    return {'project': 'ArmyCommander'}

@view_config(route_name='guide', renderer='templates/guide.jinja2')
def guide(request):
    return {'username': request.authenticated_userid, 'project': 'ArmyCommander'}

@view_config(route_name='rating', renderer='templates/rating.jinja2')
def rating(request):
    try:
	maps = DBSession.query(Map).all()
        top_db = DBSession.query(TopRating).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    if request.authenticated_userid == "admino":
    	return {'username': request.authenticated_userid, 'maps': maps, 'TopRating': top_db, 'project': 'ArmyCommander'}
    return {'maps': maps, 'TopRating': top_db, 'project': 'ArmyCommander'}


@view_config(route_name='editdatabase', context='.models.AccessGroups',
 renderer='templates/workwithdatabase.jinja2', permission='edit')
def edit_db(request):
    try:
        players = DBSession.query(Player).all() 
        maps = DBSession.query(Map).all()
    except DBAPIError:
	return Response(conn_err_msg, content_type='text/plain', status_int=500)
    user = request.authenticated_userid   
    from urlparse import parse_qs
    if request.POST:
	if "player_button" in request.params:
		max_id = len(players)
        	param = request.params["player_name"]
        	DBSession.add(Player(id=max_id,name=param))
        	players = DBSession.query(Player).all()
		return {'allmaps': maps, 'allplayers': players, 'username': user, 'information': 'player was added', 'project': 'ArmyCommander'} 
	if "map_button" in request.params: 

		max_id = len(maps)
		param = request.params["map_name"]
		DBSession.add(Map(id=max_id,name=param))
		maps = DBSession.query(Map).all()
		return {'allmaps': maps, 'allplayers': players, 'username': user, 'information': 'map was added', 'project': 'ArmyCommander'} 

    return {'allmaps': maps, 'allplayers': players, 'username': user, 'project': 'ArmyCommander'}
    


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_ArmyCommander_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

@view_config(route_name='login', renderer='templates/loginform.jinja2')
@forbidden_view_config(renderer='templates/loginform.jinja2')
def login(request):
    	if 'submitted' in request.params:
        	login = request.params['login']
        	password = request.params['password']
		if USERS.get(login) == password:
		    	headers = remember(request, login)			
            		return HTTPFound(location = 'home', headers = headers)
        	else:
    			return {'message': "Incorrect login or password", 'project': 'ArmyCommander'}
	return {'project': 'ArmyCommander'}

	
@view_config(route_name='logout')
def logout(request):
	headers = forget(request)
	return HTTPFound(location = request.referrer,
headers = headers)




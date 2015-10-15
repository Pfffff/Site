USERS = {'admin':'password',
'admino':'00000000'}

GROUPS = {'admino':['group:editors']}

def groupfinder(userid, request):
	if userid in USERS:
		return GROUPS.get(userid, [])



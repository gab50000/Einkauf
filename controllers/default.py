# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    join=db(db.req.req_id==db.item.id).select()
    items=db().select(db.item.ALL, orderby=db.item.name)
    return dict(reqs=join, items=items)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    db.auth_user.last_name.readable = db.auth_user.last_name.writable=False
    db.auth_user.first_name.readable = db.auth_user.first_name.writable=False
    #~ db.auth_user.email.readable = db.auth_user.email.writable=False
    return dict(form=auth())
@auth.requires_login()
def wunsch():
    return dict(req=db().select(db.req.ALL), items = crud.create(db.req, fields=["req_id", "quantity"]))#items=crud.create(db().select(db.req.req_id, db.req.quantity)))
@auth.requires_login()
def notieren():
    query = db.req.req_id == db.item.id == db.purchase.pur_id    
    return dict(requests=db(db.req.req_id==db.item.id).select(db.item.name, db.req.datum, db.req.quantity), \
        purchases = db(query).select(db.item.name, db.req.datum, db.purchase.datum, db.purchase.price, db.purchase.quantity), users = db().select(db.auth_user.ALL))

def test():
    query = (db.purchase.pur_id == db.item.id) & (db.req.req_id == db.item.id)

    return dict(selection = db(query).select())
    
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

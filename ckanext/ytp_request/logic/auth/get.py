import logging
from ckan import model, authz
from ckan.common import _

log = logging.getLogger(__name__)


def member_request(context, data_dict):
    """ Only allowed to sysadmins or organization admins """
    user = context.get('user')
    if not user:
        return {'success': False}

    if authz.is_sysadmin(user):
        return {'success': True}

    membership = model.Member.get(data_dict.get("mrequest_id"))
    if not membership:
        return {'success': False}

    if membership.table_name != 'user':
        return {'success': False}

    userobj = model.User.get(user)
    if not userobj:
        return {'success': False}

    query = (model.Session.query(model.Member)
                          .filter(model.Member.state == 'active')
                          .filter(model.Member.table_name == 'user')
                          .filter(model.Member.capacity == 'admin')
                          .filter(model.Member.table_id == userobj.id)
                          .filter(model.Member.group_id == membership.group_id))
    return {'success': query.count() > 0}


def member_requests_mylist(context, data_dict):
    """ Show request access check """
    # TODO: Sysadmins dont have this functionality since it is pointless. Make
    # it at the logical level
    return _only_registered_user(context)


def member_requests_list(context, data_dict):
    """ Show request access check """
    return _only_registered_user(context)


def _only_registered_user(context):
    if authz.auth_is_anon_user(context):
        return {'success': False, 'msg': _('User is not logged in')}
    return {'success': True}


def organization_list_without_memberships(context, data_dict):
    return {'success': True}

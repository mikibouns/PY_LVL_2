SERVICE_MSG = {
    'probe': {
        'action': 'probe',
    },
    'quit': {
        'action': 'quit'
    },
    '1xx': {
        100: {
            'response': 100,
            'alert': 'base info'
        },
        101: {
            'response': 101,
            'alert': 'important info'
        }
    },
    '2xx': {
        200: {
            'response': 200,
            'alert': 'OK'
        },
        201: {
            'response': 201,
            'alert': 'created'
        },
        202: {
            'response': 202,
            'alert': 'accepted'
        }
    },
    '4xx': {
        400: {
            'response': 400,
            'error': 'wrong request'
        },
        401: {
            'response': 401,
            'error': 'not authorized'
        },
        402: {
            'response': 402,
            'error': 'incorrect login or password'
        },
        403: {
            'response': 403,
            'error': 'forbidden'
        },
        404: {
            'response': 404,
            'error': 'not found'
        },
        409: {
            'response': 409,
            'error': 'Someone​ is​ already​ connected​ with​ the​ given​ user​ name'
        },
        410: {
            'response': 410,
            'error': 'offline'
        }
    },
    '5xx': {
        500: {
            'response': 500,
            'error': 'server error'
        }
    }
}

users_list = {
    'igor': {
        'passwd': '12345678',
        'status': 'authorized',
        'state': 'offline'
    },
    'maria': {
        'status': 'unauthorized',
        'state': 'online'
    },
    'vasia': {
        'passwd': '12345678',
        'status': 'authorized',
        'state': 'offline'
    },
    'elena': {
        'passwd': '12345678',
        'status': 'authorized',
        'state': 'online'
    }
}
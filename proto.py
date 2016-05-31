#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
from os import path


# base_request = {
#     'name': 'base_request',
#     'fields': [
#         {
#             'name': 'type',
#             'type': 'string'
#         },
#         {
#             'name': 'request_id',
#             'type': 'int'
#         },
#         {
#             'name': 'handler',
#             'type': 'string'
#         }
#     ]
# }

login_request = {
    'name': 'login_request',
    # 'base': 'base_request',
    'fields': [
        {
            'name': 'username',
            'type': 'string'
        },
        {
            'name': 'password',
            'type': 'string'
        },
    ]
}

login_request_response = {
    'name': 'login_request_response',
    'fields': [
        {
            'name': 'result',
            'type': 'bool'
        },
        {
            'name': 'errno',
            'type': 'int'
        }
    ]
}

create_actor_request_response = {
    'name': 'create_actor_request_response',
    'fields': [
        {
            'name': 'result',
            'type': 'bool'
        },
        {
            'name': 'errno',
            'type': 'int'
        }
    ]
}

actor = {
    'name': 'actor',
    'fields': [
        {
            'name': 'actor_id',
            'type': 'int'
        },
        {
            'name': 'name',
            'type': 'string'
        },
        {
            'name': 'level',
            'type': 'int'
        },
        {
            'name': 'gold',
            'type': 'int'
        },
        {
            'name': 'experience',
            'type': 'int'
        },
    ]
}

get_actor_info_request_response = {
    'name': 'get_actor_info_request_response',
    'fields': [
        {
            'name': 'actor_info',
            'type': 'actor',
        },
        {
            'name': 'errno',
            'type': 'int'
        }
    ]
}


def to_csharp_name(name):
    tokens = name.split('_')
    cap_tokens = [''.join([token[0].upper(), token[1:]]) for token in tokens]
    csharp_name = ''.join(cap_tokens)
    return csharp_name


def to_csharp_type(type_name):
    if type_name in ['int', 'float', 'string', 'bool']:
        return type_name
    else:
        return to_csharp_name(type_name)


def create_csharp_class(type_def, dirname):
    name = type_def.get('name')
    class_name = to_csharp_name(name)

    lines = []
    base_class = type_def.get('base', None)
    lines.append('namespace Shooter {')
    lines.append('[System.Serializable]')
    lines.append('public class {0}'.format(class_name))
    if base_class:
        lines[0] += ' : {0}'.format(to_csharp_name(base_class))

    lines.append('{')
    fields = type_def.get('fields')
    for field in fields:
        field_name = field.get('name') # to_csharp_name(field.get('name'))
        field_type = to_csharp_type(field.get('type'))
        lines.append('    public {0} {1};'.format(field_type, field_name))
    lines.append('}')
    lines.append('}')
    text = '\n'.join(lines)
    fname = '%s\%s.cs' % (dirname, class_name)
    print 'write to', fname
    with open(fname, 'w') as f:
        f.write(text)


def create_python_class(type_def, lines=[]):
    name = type_def.get('name')
    class_name = to_csharp_name(name)

    base_class = type_def.get('base', None)
    lines.append('class {0}'.format(class_name))
    if base_class:
        lines[-1] += '({0}):'.format(to_csharp_name(base_class))
    else:
        lines[-1] += ':'
    lines.append('')
    lines.append('    def __init__(self, *args):')

    fields = type_def.get('fields')
    for i, field in enumerate(fields):
        field_name = field.get('name')
        lines.append('        self.{0} = args[{1}]'.format(field_name, i))
    lines.append('')
    lines.append('    def dump(self):')
    lines.append('        ret = {}')
    for i, field in enumerate(fields):
        field_name = field.get('name')
        lines.append('        ret[\'{0}\'] = server.dump(self.{0})'.format(field_name))
    lines.append('        return ret')

    lines.append('')
    lines.append('')


print 'generate c# class for message(request/response)'
dirname = 'generated'
if path.isdir(dirname):
    shutil.rmtree(dirname)

os.mkdir(dirname)
# create_csharp_class(base_request, dirname)
create_csharp_class(login_request, dirname)
create_csharp_class(login_request_response, dirname)
create_csharp_class(create_actor_request_response, dirname)
create_csharp_class(actor, dirname)
create_csharp_class(get_actor_info_request_response, dirname)
print 'done'

print 'generate python class for message(request/response)'
lines = []
lines.append('import server')
lines.append('')
lines.append('')
create_python_class(login_request, lines)
create_python_class(login_request_response, lines)
create_python_class(create_actor_request_response, lines)
create_python_class(actor, lines)
create_python_class(get_actor_info_request_response, lines)
with open('message.py', 'w') as f:
    text = '\n'.join(lines)
    f.write(text)
print 'done'

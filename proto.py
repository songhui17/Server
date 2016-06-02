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

type_map = {
    'login_request': {
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
    },

    'login_request_response': {
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
    },

    'get_account_info_request': {
        'name': 'get_account_info_request',
        'fields': [
            {
                'name': 'username',
                'type': 'string',
            }
        ]
    },

    'account': {
        'name': 'account',
        'fields': [
            {
                'name': 'name',
                'type': 'string',
            },
            {
                'name': 'actor_id',
                'type': 'int',
            }
        ]
    },

    'get_account_info_request_response': {
        'name': 'get_account_info_request_response',
        'fields': [
            {
                'name': 'account_info',
                'type': 'account'
            },
            {
                'name': 'errno',
                'type': 'int'
            }
        ]
    },

    'create_actor_request': {
            'name': 'create_actor_request',
            'fields': [
                {
                    'name': 'username',
                    'type': 'string'
                },
                {
                    'name': 'actor_type',
                    'type': 'string',
                }
        ]
    },

    'create_actor_request_response': {
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
    },

    'actor': {
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
    },

    'get_actor_info_request': {
        'name': 'get_actor_info_request',
        'fields': [
            {
                'name': 'username',
                'type': 'string'
            }
        ]
    },

    'get_actor_info_request_response': {
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
    },

    'get_actor_level_info_request': {
        'name': 'get_actor_level_info_request',
        'fields': [
            {
                'name': 'username',
                'type': 'string'
            },
        ]
    },

    'actor_level_info': {
        'name': 'actor_level_info',
        'fields': [
             {
                'name': 'actor_id',
                'type': 'int'
             },
             {
                 'name': 'level_id',
                 'type': 'int'
             },
             {
                 'name': 'passed',
                 'type': 'bool'
             },
             {
                 'name': 'star1',
                 'type': 'bool'
             },
             {
                 'name': 'star2',
                 'type': 'bool'
             },
             {
                 'name': 'star3',
                 'type': 'bool'
             },
        ]
    },

    'get_actor_level_info_request_response': {
        'name': 'get_actor_level_info_request_response',
        'fields': [
            {
                'name': 'actor_level_info',
                'type': 'list actor_level_info'
            },
            {
                'name': 'errno',
                'type': 'int'
            }
        ]
    },
    'get_level_info_request': {
        'name': 'get_level_info_request',
        'fields': [
            {
                'name': 'username',
                'type': 'string'
            }
        ]
    },
    'level_info': {
        'name': 'level_info',
        'fields': [
            {
                'name': 'level_id',
                'type': 'int'
            },
            {
                'name': 'title',
                'type': 'string'
            },
            {
                'name': 'task1',
                'type': 'string'
            },
            {
                'name': 'task2',
                'type': 'string'
            },
            {
                'name': 'task3',
                'type': 'string'
            },
            {
                'name': 'bonuses',
                'type': 'list string'
            }
        ]
    },
    'get_level_info_request_response': {
        'name': 'get_level_info_request_response',
        'fields': [
            {
                'name': 'level_info',
                'type': 'list level_info'
            },
            {
                'name': 'errno',
                'type': 'int'
            }
        ]
    },
    'start_level_request' : {
        'name': 'start_level_request',
        'fields': [
            {
                'name': 'actor_id',
                'type': 'int'
            },
            {
                'name': 'level_id',
                'type': 'int'
            }
        ]
    },
    'start_level_request_response' : {
        'name': 'start_level_request_response',
        'fields': [
            {
                'name': 'errno',
                'type': 'int'
            }
        ]
    },
    'vector3': {
        'name': 'vector3',
        'fields': [
            {
                'name': 'x',
                'type': 'float'
            },
            {
                'name': 'y',
                'type': 'float'
            },
            {
                'name': 'z',
                'type': 'float'
            },
        ]
    },
    'spawn_bot_request': {
        'name': 'spawn_bot_request',
        'fields': [
            {
                'name': 'bot_id',
                'type': 'int'
            },
            {
                'name': 'bot_type',
                'type': 'string'
            },
            {
                'name': 'position',
                'type': 'vector3'
            },
            {
                'name': 'rotation',
                'type': 'float'
            }
        ]
    },
    'spawn_bot_request_response': {
        'name': 'spawn_bot_request_response',
        'fields': [
            {
                'name': 'errno',
                'type': 'int'
            }
        ]
    }
}

def to_csharp_name(name):
    tokens = name.split('_')
    cap_tokens = [''.join([token[0].upper(), token[1:]]) for token in tokens]
    csharp_name = ''.join(cap_tokens)
    return csharp_name


def is_primitive(type_name):
    return type_name in ['int', 'float', 'string', 'bool']


def to_csharp_type(type_name):
    if type_name in ['int', 'float', 'string', 'bool']:
        return type_name
    else:
        if type_name.startswith('list '):
            
            return 'List<%s>' % to_csharp_name(type_name[4:].strip())
        else:
            return to_csharp_name(type_name)


def create_csharp_class(type_def, dirname,
                        responses=[], des_template='',
                        requests=[], req_template=''):
    # import pdb; pdb.set_trace()

    name = type_def.get('name')
    class_name = to_csharp_name(name)

    class_template = '''using System;
using System.Collections.Generic;

namespace Shooter
{
    [Serializable]
    public class %s {
%s
        public override string ToString() {
            var info = "";
%s
            return info;
        }
    }
%s
'''
    field_template = '''        public %s %s; '''
    
    to_string_template = r'''            info += "<b>%s</b>:" + %s + "\n";'''
    to_string_template_2 = r'''            info += "<b>%s</b>:\n" + %s + "\n";'''

    lines = []
    base_class = type_def.get('base', None)
    class_name_xxx = class_name
    if base_class:
        base_class = to_csharp_name(base_class)
        class_name_xxx = '%s : %s' % (class_name_xxx, base_class)

    fields = type_def.get('fields')
    fields_xxx = []
    to_string_xxx = []
    for field in fields:
        field_name = field.get('name') # to_csharp_name(field.get('name'))
        field_type = to_csharp_type(field.get('type'))
        fields_xxx.append(field_template % (field_type, field_name))
        if is_primitive(field_type):
            to_string_xxx.append(to_string_template % (field_name, field_name))
        else:
            to_string_xxx.append(to_string_template_2 % (field_name, field_name))

    wrap_template = '''
    [Serializable]
    public class _%s {
        public string handler;
        public string type;
        public int request_id;
        public %s response;
    }
}'''

    # response wrapper
    wrap_class = '}'
    if name.endswith('response'):
        wrap_class = wrap_template % (class_name, class_name)
        des = des_template % (name, class_name, class_name)
        responses.append(des)

    # request handler
    if name.endswith('request'):
        req = req_template % (name,
                              class_name, class_name,
                              class_name,
                              class_name,
                              class_name)
        requests.append(req)

    text = class_template % (class_name_xxx,
                             '\n'.join(fields_xxx),
                             '\n'.join(to_string_xxx),
                             wrap_class)
    fname = '%s\%s.cs' % (dirname, class_name)
    print 'write to', fname,
    with open(fname, 'w') as f:
        f.write(text)
    print 'done'


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

deserializer_template = r'''using UnityEngine;

namespace Shooter
{
    public class ResponseDeserializer {
        public static object Deserialize(string handler_, string payload_, out int requestId_) {
            %s
            requestId_ = -1;
            return null;
        }
    }

    public class RequestHandlerDispatcher {
        public static bool HandleRequest(SockUtil sockUtil_, IRequestHandler h_, string handler_, string payload_) {
            %s
            return false;
        }
    }
}
'''
deserialize_case_tempalate = r'''
            if (handler_ == "%s") {
                var response = JsonUtility.FromJson<_%s>(payload_) as _%s;
                requestId_ = response.request_id;
                return response.response;
            }
'''
handle_request_template = r'''
            if (handler_ == "%s") {
                var request = JsonUtility.FromJson<BaseRequest<%s>>(payload_) as BaseRequest<%s>;
                var requestId = request.request_id;
                var requireResponse = request.require_response;
                var ret = h_.RecvMessage(request.request) as %sResponse;
                if (requireResponse) {
                    var xxx_response = new _%sResponse() {
                        handler = string.Format("{0}_response", handler_),
                        type = "response",
                        request_id = requestId,
                        response = ret,
                    };
                    sockUtil_.SendMessage<_%sResponse>(xxx_response, xxx_response.handler);
                }
                return true;
            }
'''

responses = []
requests = []
for k, v in type_map.iteritems():
    create_csharp_class(v, dirname,
                        responses, deserialize_case_tempalate,
                        requests, handle_request_template)
print 'done'

des_fname = '%s/ResponseDeserializer.cs' % dirname
print 'write to', des_fname
with open(des_fname, 'w') as f:
    text = ''.join(responses)
    text2 = ''.join(requests)
    f.write(deserializer_template % (text, text2))

print 'generate python class for message(request/response)'
lines = []
lines.append('import server')
lines.append('')
lines.append('')
for k, v in type_map.iteritems():
    create_python_class(v, lines)

with open('message.py', 'w') as f:
    text = '\n'.join(lines)
    f.write(text)
print 'done'

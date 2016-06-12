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
            {
                'name': 'max_hp',
                'type': 'int'
            },
            {
                'name': 'hp',
                'type': 'int'
            },
            {
                'name': 'max_ammo',
                'type': 'int'
            },
            {
                'name': 'ammo',
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
    'actor_level_info_sync_request': {
        'name': 'actor_level_info_sync_request',
        'fields': [
            {
                'name': 'actor_level_info',
                'type': 'actor_level_info'
            }
        ]
    },
    'actor_level_info_sync_request_response': {
        'name': 'actor_level_info_sync_request_response',
        'fields': [
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
    },
    'enter_level_request': {
        'name': 'enter_level_request',
        'fields': [
        ]
    },
    'enter_level_request_response': {
        'name': 'enter_level_request_response',
        'fields': [
            {
                'name': 'errno',
                'type': 'int'
            }
        ]
    },
    'finish_level_request': {
        'name': 'finish_level_request',
        'fields': [
            {
                'name': 'win',
                'type': 'bool'
            },
            {
                'name': 'bonuses',
                'type': 'list string'
            }
        ]
    },
    'finish_level_request_response': {
        'name': 'finish_level_request_response',
        'fields': [
            {
                'name': 'errno',
                'type': 'int'
            }
        ]
    },
    'leave_level_request': {
        'name': 'leave_level_request',
        'fields': [
        ]
    },
    'leave_level_request_response': {
        'name': 'leave_level_request_response',
        'fields': [
            {
                'name': 'errno',
                'type': 'int'
            }
        ]
    },
    'level0_bot_killed_request': {
        'name': 'level0_bot_killed_request',
        'fields': [
            {
                'name': 'bot_id',
                'type': 'int'
            }
        ]
    },
    'level0_bot_killed_request_response': {
        'name': 'level0_bot_killed_request_response',
        'fields': [
            {
                'name': 'errno',
                'type': 'int'
            }
        ]
    },
    'bot_transform_sync_request': {
        'name': 'bot_transform_sync_request',
        'fields': [
            {
                'name': 'bot_id',
                'type': 'int'
            },
            {
                'name': 'position',
                'type': 'vector3'
            },
            {
                'name': 'rotation',
                'type': 'float'
            },
            {
                'name': 'waypoint_position',
                'type': 'vector3'
            }
        ]
    },
    'bot_transform_sync_request_response': {
        'name': 'bot_transform_sync_request_response',
        'fields': [
        ]
    },
    'bot_explose_request': {
        'name': 'bot_explose_request',
        'fields': [
            {
                'name': 'bot_id',
                'type': 'int'
            }
        ]
    },
    'bot_explose_request_response': {
        'name': 'bot_explose_request_response',
        'fields': [
        ]
    },
    'bot_play_animation_request': {
        'name': 'bot_play_animation_request',
        'fields': [
            {
                'name': 'bot_id',
                'type': 'int'
            },
            {
                'name': 'animation_clip',
                'type': 'string'
            }
        ]
    },
    'bot_play_animation_request_response': {
        'name': 'bot_play_animation_request_response',
        'fields': [
        ]
    },
    'tower_hp_sync_request': {
        'name': 'tower_hp_sync_request',
        'fields': [
            {
                'name': 'tower_id',
                'type': 'int'
            },
            {
                'name': 'hp',
                'type': 'int'
            },
            {
                'name': 'max_hp',
                'type': 'int'
            }
        ]
    },
    'tower_hp_sync_request_response': {
        'name': 'tower_hp_sync_request_response',
        'fields': [
        ]
    },
    'update_actor_hp_request': {
        'name': 'update_actor_hp_request',
        'fields': [
            {
                'name': 'actor_id',
                'type': 'int'
            },
            {
                'name': 'hp',
                'type': 'int'
            },
            {
                'name': 'max_ammo',
                'type': 'int'
            },
            {
                'name': 'ammo',
                'type': 'int'
            }
        ]
    },
    'update_actor_hp_request_response': {
        'name': 'update_actor_hp_request_response',
        'fields': [
            {
                'name': 'errno',
                'type': 'int'
            }
        ]
    },
    'spawn_item_request': {
        'name': 'spawn_item_request',
        'fields': [
            {
                'name': 'item_type',
                'type': 'string'
            },
            {
                'name': 'position',
                'type': 'vector3'
            }
        ]
    },
    'spawn_item_request_response': {
        'name': 'spawn_item_request_response',
        'fields': [
        ]
    },
    'use_item_request': {
        'name': 'use_item_request',
        'fields': [
            {
                'name': 'item_type',
                'type': 'string'
            },
        ]
    },
    'use_item_request_response': {
        'name': 'use_item_request_response',
        'fields': [
        ]
    },
    'kill_report': {
        'name': 'kill_report',
        'fields': [
            {
                'name': 'double_kill', 
                'type': 'int',
            },
            {
                'name': 'triple_kill',
                'type': 'int'
            }
        ]
    },
    'kill_report_sync_request': {
        'name': 'kill_report_sync_request',
        'fields': [
            {
                'name': 'actor_id',
                'type': 'int'
            },
            {
                'name': 'kill_report',
                'type': 'kill_report'
            }
        ]
    },
    'kill_report_sync_request_response': {
        'name': 'kill_report_sync_request_response',
        'fields': [
        ]
    }
}

errno = [
    {
        'name': 'E_OK',
        'value': 0,
        'doc': 'success'
    },
    {
        'name': 'E_NO_USERNAME',
        'value': 1,
        'doc': 'no account with name username'
    },
    {
        'name': 'E_INVALID_PASSWORD',
        'value': 2,
        'doc': 'invalid password'
    },
    {
        'name': 'E_USER_NOT_LOGINED',
        'value': 3,
        'doc': 'user has not logined, login required'
    },
    {
        'name': 'E_ACTOR_EXIST',
        'value': 4,
        'doc': 'actor already bound to account'
    },
    {
        'name': 'E_ACTOR_NOT_CREATED',
        'value': 5,
        'doc': 'actor_id == -1, no actor bound to account'
    },
    {
        'name': 'E_NO_SUCH_LEVEL',
        'value': 6,
        'doc': 'invalid level id'
    },
    {
        'name': 'E_LEVEL_NOT_ALLOWED',
        'value': 7,
        'doc': 'invalid level id'
    },
]

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


def to_python_type(type_name):
    if type_name in ['int', 'float', 'bool']:
        return type_name
    elif type_name == 'string':
        return 'str'
    else:
        if type_name.startswith('list '):
            
            return '%s[]' % to_python_type(type_name[4:].strip())
        else:
            return to_csharp_name(type_name)

def create_csharp_class(type_def, dirname,
                        responses=[], des_template='',
                        requests=[], req_template='',
                        sockutil_items=[]):
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

    sockutil_request_item_template = '''    public static int %s(%s request_, Action<%sResponse, int> callback_ = null) {
        return SockUtil.Instance.SendRequest<%s, %sResponse>("%s", request_, callback_);
    }
'''
    # sockutil_items = []
    # request handler
    if name.endswith('request'):
        req = req_template % (name,
                              class_name, class_name,
                              class_name,
                              class_name,
                              class_name)
        requests.append(req)

        sockutil_items.append(sockutil_request_item_template %\
            (class_name[0:-7], class_name, class_name,\
            class_name, class_name, name[0:-8]))

    text = class_template % (class_name_xxx,
                             '\n'.join(fields_xxx),
                             '\n'.join(to_string_xxx),
                             wrap_class)
    fname = '%s.cs' % path.join(dirname, class_name)
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

    init_no_field = '''
    def __init__(self):
        pass'''

    init_template='''
    def __init__(self, **kwargs):
        """
        Params:

%s

        """
%s'''

    doc_param_item_template='''        %s: %s'''
    init_item_template='''        self.%s = kwargs.get('%s')'''

    load_no_field = '''
    def load(self):
        pass'''

    load_template='''
    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
%s'''

    load_item_template='''        self.%s = kwargs['%s']'''

    dump_no_field = '''
    def dump(self):
        return {}'''

    dump_template = '''
    def dump(self):
        """dump -> dict
        """
        ret = {}
%s
        return ret'''

    dump_item_template='''        ret['%s'] = sockutil.dump(self.%s)'''

    fields = type_def.get('fields')
    if len(fields) > 0:
        init_items = []
        doc_param_items = []
        load_items = []
        dump_items = []
        for field in fields:
            field_name = field['name']
            field_type = to_python_type(field['type'])
            init_items.append(init_item_template % (field_name, field_name))
            doc_param_items.append(
                doc_param_item_template % (field_name, field_type))
            load_items.append(load_item_template % (field_name, field_name))
            dump_items.append(dump_item_template % (field_name, field_name))

        init = init_template % ('\n'.join(doc_param_items), '\n'.join(init_items))
        load = load_template % '\n'.join(load_items)
        dump = dump_template % '\n'.join(dump_items)
        lines.append(init) 
        lines.append(load) 
        lines.append(dump) 
    else:
        lines.append(init_no_field)
        lines.append(load_no_field)
        lines.append(dump_no_field)


    lines.append('')
    lines.append('')


def create_python_errno(errno_list, fname):
    python_template = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = [
%s
]


%s
'''
    export_item_template = '''    '%s','''
    enum_item_template = '''%s = %d               # %s'''
    export_items = []
    enum_items = []
    for err in errno_list:
        export_items.append(export_item_template % err['name'])
        enum_items.append(
            enum_item_template % (err['name'], err['value'], err['doc']))

    with open(fname,'w') as f:
        text = python_template % ('\n'.join(export_items),
                                  '\n'.join(enum_items))
        f.write(text)


def create_csharp_errno(errno_list, fname):
    csharp_template = '''namespace Shooter
{
    public enum ENUM_SHOOTER_ERROR {
%s
    }
}
'''
    enum_item_template = '''        %s = %d,              // %s'''
    enum_items = []
    for err in errno_list:
        enum_items.append(
            enum_item_template % (err['name'], err['value'], err['doc']))

    with open(fname,'w') as f:
        text = csharp_template % '\n'.join(enum_items)
        f.write(text)


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
sockutil_items = []
for k, v in type_map.iteritems():
    create_csharp_class(v, dirname,
                        responses, deserialize_case_tempalate,
                        requests, handle_request_template,
                        sockutil_items)
print 'done'

des_fname = path.join(dirname, 'ResponseDeserializer.cs')
print 'write to', des_fname
with open(des_fname, 'w') as f:
    text = ''.join(responses)
    text2 = ''.join(requests)
    f.write(deserializer_template % (text, text2))

sockutil_template = '''
using System;
using Shooter;

public partial class SockUtil {
%s
}
'''
sockutil_fname = path.join(dirname, 'SockUtilSendRequests.cs')
print 'write to', sockutil_fname
with open(sockutil_fname, 'w') as f:
    text = sockutil_template % '\n'.join(sockutil_items)
    f.write(text)

print 'generate python class for message(request/response)'
lines = []
lines.append('import sockutil')
lines.append('')
lines.append('')
for k, v in type_map.iteritems():
    create_python_class(v, lines)

with open('message.py', 'w') as f:
    text = '\n'.join(lines)
    f.write(text)


print 'generate c# errno'
create_csharp_errno(errno, path.join(dirname, 'Errno.cs'))

print 'generate python errno'
create_python_errno(errno, 'servererrno.py')



print 'done'

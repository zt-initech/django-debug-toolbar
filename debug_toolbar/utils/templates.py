from __future__ import absolute_import, unicode_literals

try:
    from importlib import import_module
except ImportError:  # python 2.6
    from django.utils.importlib import import_module
import inspect
import os.path
import re
import sys
try:
    import threading
except ImportError:
    threading = None

import django
from django.template import Node
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils import six
from django.views.debug import linebreak_iter


def get_template_info():
    template_info = None
    cur_frame = sys._getframe().f_back
    try:
        while cur_frame is not None:
            in_utils_module = cur_frame.f_code.co_filename.endswith(
                "/debug_toolbar/utils.py"
            )
            is_get_template_context = (
                cur_frame.f_code.co_name == get_template_context.__name__
            )
            if in_utils_module and is_get_template_context:
                # If the method in the stack trace is this one
                # then break from the loop as it's being check recursively.
                break
            elif cur_frame.f_code.co_name == 'render':
                node = cur_frame.f_locals['self']
                if isinstance(node, Node):
                    template_info = get_template_context(node.source)
                    break
            cur_frame = cur_frame.f_back
    except Exception:
        pass
    del cur_frame
    return template_info


def get_template_context(source, context_lines=3):
    line = 0
    upto = 0
    source_lines = []
    # before = during = after = ""

    origin, (start, end) = source
    template_source = origin.reload()

    for num, next in enumerate(linebreak_iter(template_source)):
        if start >= upto and end <= next:
            line = num
            # before = template_source[upto:start]
            # during = template_source[start:end]
            # after = template_source[end:next]
        source_lines.append((num, template_source[upto:next]))
        upto = next

    top = max(1, line - context_lines)
    bottom = min(len(source_lines), line + 1 + context_lines)

    context = []
    for num, content in source_lines[top:bottom]:
        context.append({
            'num': num,
            'content': content,
            'highlight': (num == line),
        })

    return {
        'name': origin.name,
        'context': context,
    }

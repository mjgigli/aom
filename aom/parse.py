#!/usr/bin/env python
#
#  @file  parse.py
#
#
#
#  COPYRIGHT:
#
#     Copyright: TrellisWare Technologies Inc., 2017:
#     Notice: TrellisWare Proprietary Information
#             All contents of this file are to be treated as
#             Proprietary Information and shall not be disclosed to
#             any third party without the express permission from
#             TrellisWare.
#
#  RESTRICTED RIGHTS (Required):
#
#     THIS SECTION IS NOT APPLICABLE TO THIS MODULE
#     (THIS MODULE IS NOT A DELIVERABLE ITEM)
#
#     Contract No.: XXXXXX-XX-X-XXXX
#     Contractor Name: TrellisWare Technologies Inc.
#     Contractor Address:  ADDRESS_TBD
#
#     The Government's right to use, modify, reproduce, release,
#     perform, display, or disclose this software are restricted by
#     paragraph XX of the Rights in Noncommercial Computer Software
#     and Noncommercial Computer Software clause contained in the
#     above identified contract.  Any reproduction of computer
#     software or portions thereof marked with this legend must also
#     reproduce the markings.  Any person, other than the Government,
#     who has been provided access to such data must promptly notify
#     the above named Contractor.
#
#  @author
#  @date    09-28-2017
#
#  @version $Id$
#
#  $URL$
#

import xmltodict


def parse_xml(filename):
    with open(filename) as f:
        project = xmltodict.parse(f.read())

    return project


def get_list(node):
    if isinstance(node, list):
        return node
    else:
        return [node]


def get_child_list(node, attr):
    try:
        attrs = get_list(node[attr])
    except KeyError:
        attrs = None
    return attrs


class node(object):
    def __init__(self, n):
        self._name = n['@name']
        try:
            self._comments = a['documentation']
        except KeyError:
            pass


class attr_node(node):
    def __init__(self, a):
        super(attr_node, self).__init__(a)
        self._value = None


class operation_node(node):
    def __init__(self, o):
        super(operation_node, self).__init__(o)
        self._params = get_child_list(o, 'parameter')
        self._code = o['code']


class class_node(node):
    def __init__(self, c):
        super(class_node, self).__init__(c)
        self._superclass = c['superclass']

        # parse attrs

        # parse operations


class ao_node(class_node):
    pass


if __name__ == '__main__':
    project = parse_xml('/home/mgigli/test.qm')

    model = project['model']
    packages = get_child_list(model, 'package')
    try:
        # parse each package in project
        for p in packages:
            print 'Parsing', p['@name']
            p.classes = get_child_list(p, 'class')
            if p.classes is not None:
                print 'Classes: %s' % ([(c['@name'], c['@superclass']) for c in p.classes])
            p.attributes = get_child_list(p, 'attribute')
            if p.attributes is not None:
                print 'Attributes: %s' % (len(p.attributes),)
            p.operations = get_child_list(p, 'operation')
            if p.operations is not None:
                print 'Operations: %s' % (len(p.operations),)
    except TypeError:
        print 'No packages in the model'

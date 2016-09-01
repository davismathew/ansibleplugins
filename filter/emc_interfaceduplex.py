# (c) 2014, Brian Coca <bcoca@ansible.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import math
import collections
import json
from ansible import errors

class Error(Exception):
    """

    """
class ConstructvarError(Exception):
    """

    """

class JSONFilterForDuplex(object):
    def compare_duplexjson(self,variable):
        flag = True
        retdict={}
        list=[]
        olddict={}
        newdict={}
        nestlist=[]

        if not variable:
            return "command o/p empty"

        for i,val in enumerate(variable):
            try:
                if variable[i]['duplex'] == 'Half':
                    flag = False
                    list.append(construct_var(variable[i]))
            except Exception, err:
                return str(err)
            if(len(list)>0):
                retdict["half duplex interfaces"] = list
                list=[]


        if(flag):
            return "No Half duplex interfaces found"
        else:
            return retdict

        return flag



def compareduplexoutput(outputvariable):
    jfilter = JSONFilterForDuplex()

    return jfilter.compare_duplexjson(outputvariable)


def getvars_file(command,file):
    try:
        with open(file) as data_file:
            data=json.load(data_file)
    except:
        raise errors.AnsibleFilterError('file parse error')
#        return "file parse error"
    varlist=[]
    try:
        for key,value in data[command].iteritems():
            if (data[command][key] == "yes"):
                varlist.append(key)
    except:
        raise errors.AnsibleFilterError('key list error')
    return varlist

def construct_var(variable):
    base_path='/etc/'
    file='/home/davis/Documents/networkaut/disp.json'
    var={}
    olddict={}
    newdict={}
    innerlist=[]
    varlist = getvars_file('show interfaces',base_path+'disp.json')
    try:
        for ele in varlist:
            var[ele]=variable[ele]
        innerlist = [var]
    except:
        raise errors.AnsibleFilterError('error in construct_var')
#        return "error in construct_var"
#    var={}

    return var



def compare_duplex(regvariable,filename):

    base_path='/etc/'
    outdict={}
    test=[]
    for key,value in regvariable.iteritems():
        # path_var = getvars_file(key,base_path+filename)
        outdict[key]=compareduplexoutput(regvariable[key])
    return outdict

def compare_variable(regvariable,variable):

    base_path='/etc/'
    outdict={}
    test=[]
    for key,value in regvariable.iteritems():
        # path_var = getvars_file(key,base_path+filename)
        outdict[key]=compareduplexoutput(regvariable[key])
    return outdict

class FilterModule(object):
    ''' Ansible math jinja2 filters '''

    def filters(self):
        return {
            # general math
            'check_duplex': compare_duplex,
            'check_variable': compare_variable,

        }

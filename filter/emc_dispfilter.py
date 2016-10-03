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

class JSONFilter(object):
    def compare_dispjson(self,variableb, variablea, argslist, command, vrf):
        flag = True
        retdict={}
        list=[]
        olddict={}
        newdict={}
        nestlist=[]
        extravars=[]

        if not variableb:
            return "second command o/p empty"
        elif not variablea:
            return "first command o/p empty"


        for element in argslist:
            for i,val in enumerate(variablea):
                try:
                    if variablea[i][element] != variableb[i][element]:
                        flag = False
                        extravars.append(element)
                        # list.append(construct_var(variableb[i],variablea[i],command))
                except Exception, err:
                    return str(err)


        for element in argslist:
            for i,val in enumerate(variablea):
                try:
                    if variablea[i][element] != variableb[i][element]:
                        flag = False
                        list.append(construct_dispvar(variableb[i],variablea[i],command,extravars,vrf))
                except Exception, err:
                    return str(err)
            if(len(list)>0):
                retdict["before,after"] = list
                list=[]


        if(flag):
            return "Success"
        else:
            return retdict

        return flag


def comparedispoutputforvrf(bef_variable,aft_variable,params_compared,command,vrf):
    jfilter = JSONFilter()

    return jfilter.compare_dispjson(bef_variable,aft_variable,params_compared,command,vrf)

def comparedispoutput(bef_variable,aft_variable,params_compared,command):
    jfilter = JSONFilter()

    return jfilter.compare_dispjson(bef_variable,aft_variable,params_compared,command,vrf='')

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

def getvrf_vars(command,file):
    try:
        with open(file) as data_file:
            data=json.load(data_file)
    except:
        raise errors.AnsibleFilterError('file parse error')
#        return "file parse error"
    varlist=[]
    command = "show ip route vrf summary"
    try:
        for key,value in data[command].iteritems():
            if (data[command][key] == "yes"):
                varlist.append(key)
    except:
        raise errors.AnsibleFilterError('key list error')
    return varlist

def construct_dispvar(variableb, variablea, command, extravars,vrf):
    base_path='/etc/'
    file='/home/davis/Documents/networkaut/disp.json'
    varb={}
    vara={}
    olddict={}
    newdict={}
    innerlist=[]
    if vrf:
    	command="show ip route vrf summary"
    varlist = getvars_file(command,base_path+'disp.json')
    varlist.extend(extravars)
    try:
        for ele in varlist:
            varb[ele]=variableb[ele]
            vara[ele]=variablea[ele]
        innerlist = [vara, varb]
    except:
        raise errors.AnsibleFilterError('error in construct_var')
#        return "error in construct_var"
    varb={}
    vara={}

    return innerlist



def compare_dispjson(b_regvar,a_regvar,filename):

    base_path='/etc/'
    outdict={}
    test=[]
    for key,value in b_regvar.iteritems():
        path_var = getvars_file(key,base_path+filename)
        outdict[key]=comparedispoutput(b_regvar[key],a_regvar[key],path_var,key)
    return outdict


def compare_dispfile(b_regvar,a_regvar,filename):
    base_path='/etc/'
    outdict={}
    test=[]
    with open(b_regvar) as data_file:
        b_regvar = json.load(data_file)

    for key,value in b_regvar.iteritems():
        path_var = getvars_file(key,base_path+filename)
        outdict[key]=comparedispoutput(b_regvar[key],a_regvar[key],path_var,key)
    return outdict

def compare_vrffile(b_regvar,a_regvar,filename):
    base_path='/etc/'
    outdict={}
    vrf = True
    test=[]
    with open(b_regvar) as data_file:
        b_regvar = json.load(data_file)
    
    for key,value in b_regvar.iteritems():
        path_var = getvrf_vars(key,base_path+filename)
        outdict[key]=comparedispoutputforvrf(b_regvar[key],a_regvar[key],path_var,key,vrf)
	if outdict[key]=="second command o/p empty":
		del outdict[key]
    return outdict

class FilterModule(object):
    ''' Ansible math jinja2 filters '''

    def filters(self):
        return {
            # emc custom compare
	    'emc_vrffilecompare': compare_vrffile,
            'emc_dispcompare': compare_dispjson,
            'emc_dispfilecompare': compare_dispfile,
        }

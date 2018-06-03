# -*- coding: utf-8 -*-
from ruamel.yaml import YAML
import subprocess
import json
import requests
import re
from functools import partial
yaml = YAML()
yaml.allow_duplicate_keys = True


def git_pull(decor, data):
    def git(*args):
        branch = data['ref']
        branch_replace = branch.__str__().replace('refs/heads/', '')
        git_pull = subprocess.call(("cd /home/demm/variables/ && git checkout %s && git pull" % branch_replace), shell=True)
        if git_pull == 0:
            return decor(*args)
    return git

def default_dict(fun):
    def create_dict():
        default_environment = {}
        other_environment = {}
        fun.func_globals['default_environment'] = default_environment
        fun.func_globals['other_environment'] = other_environment
        fun
    return create_dict()

class ConsulApplications(object):
    def __init__(self):
        self.DEFAULT_ENVIRONMENT = 'default_environment'
        self.DEFAULT_LOCATION = 'default_location'
        self.DEFAULT_NODE = 'default_node'
        self.DEFAULT_APP = 'application'

        global app
        global env
        global loc
        global nod
        app = self.DEFAULT_APP
        env = self.DEFAULT_ENVIRONMENT
        loc = self.DEFAULT_LOCATION
        nod = self.DEFAULT_NODE

    replace_by_path = lambda self, path: path.replace("u'", "").replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
    replace_by_service_name = lambda self, path: ','.join(re.sub("[][]", '', str(path)).split('/')[-1:]).replace("u'", "").replace("'", "").replace(".yml","")
    #replace_by_service_tags = lambda self, z: ','.join(re.sub("", '', str(z)).split(',')[:-1]).replace("u'", "").replace("'", "")
    replace_by_service_tags = lambda self, z: z.__str__().replace("u'", "").replace("'", "").replace("[","").replace("]","")

    def merge_environment(self, other, default):
        if isinstance(other, dict) and isinstance(default, dict):
            for k, v in default.iteritems():
                if k not in other:
                    other[k] = v
                else:
                    other[k] = self.merge_environment(other[k], v)

        return other

    def hell(self, service_name, stream, service_tags):
        default_environment = {}
        other_environment = {}

        default_environment.update(stream[app][service_name][env])
        other_environment.update(stream[app][service_name][service_tags])
        merge = self.merge_environment(other_environment, default_environment)
        return merge

    def location(self, service_name, service_tags, datacenter, environment=None, stream=None):
        if stream:
            default_environment = {}
            other_environment = {}
            default_environment.update(
                stream[app][service_name][env][loc])
            other_environment.update(
                stream[app][service_name][env][datacenter])
            merge = self.merge_environment(other_environment, default_environment)
        elif environment:
            default_environment = {}
            other_environment = {}
            default_environment.update(
                environment[loc])
            other_environment.update(
                environment[datacenter])
            merge = self.merge_environment(other_environment, default_environment)
        return merge

    def node(self, service_tags, node_name, service_name, environment=None, stream=None):
            if stream:
                default_environment = {}
                other_environment = {}
                default_environment.update(
                    stream[app][service_name][env][loc][nod])
                other_environment.update(
                    stream[app][service_name][env][loc][node_name])
                merge = self.merge_environment(other_environment, default_environment)
            elif environment:
                default_environment = {}
                other_environment = {}
                default_environment.update(environment[loc][nod])
                other_environment.update(environment[loc][node_name])
                merge = self.merge_environment(other_environment, default_environment)
            return merge

    # хуяк хуяк, архитектура приложения

    def enumeration(self, service_tags, stream, service_name, datacenter, node_name):

        if service_tags in stream[app][service_name]:
            print 1
            environment = self.hell(service_name, stream, service_tags)
            result = environment
            if datacenter in environment:
                print 2
                location = self.location(service_name, service_tags, datacenter, environment, stream=None)
                result = location
                if node_name in location:
                    print 3
                    node_dict = {self.DEFAULT_LOCATION: location}
                    node = self.node(service_tags, node_name, service_tags, node_dict, stream=None)

                    result = node
            elif node_name in environment[self.DEFAULT_LOCATION]:
                print 4
                node = self.node(service_tags, node_name, service_name, environment, stream=None)
                result = node
                return self.srv(result, service_name)
            return self.srv(result, service_name)

        elif datacenter in stream[app][service_name][env]:
            print 5
            location = self.location(service_name, service_tags, datacenter, environment=None, stream=stream)
            result = location
            if node_name in location:
                node_dict = {self.DEFAULT_LOCATION: location}
                node = self.node(service_tags, node_name, service_name, node_dict, stream=None)
                result = node
            return self.srv(result, service_name)

        elif node_name in stream[app][service_name][env][loc]:
            print 6
            node = self.node(service_tags, node_name, service_name, environment=None, stream=stream)
            result = node
            return self.srv(result, service_name)

    def get(self, data):
        real_decor = partial(git_pull, data=data)
        @real_decor
        def get_items(self, data):
            path_list = data['commits'][0]['modified']
            path_list.__str__().split(',')
            for path in path_list:
                path_replace = self.replace_by_path(path)
                # service_name = self.replace_by_service_name(path.__str__().split('/')[-1:])
                service_name = self.replace_by_service_name(path)
                if 'hive/applications' in path_replace:
                    try:
                        stream = yaml.load(open('/home/demm/variables/%s' % path_replace))
                    except TypeError:
                        continue
                    # url = "http://192.168.0.126:8500/v1/catalog/service/"+service_name+""
                    url = "http://192.168.0.126:8500/v1/catalog/service/CommonIntegration"
                    #url = "http://192.168.0.126:8500/v1/catalog/service/api_pvz"
                    data_json = requests.get(url).json()
                    if not data_json:
                        continue
                    for item in data_json:
                            node_name = (item['Node'])
                            z = (item['ServiceTags'])
                            datacenter = (item['Datacenter'])
                            service_tags = self.replace_by_service_tags(z)
                            rezult = self.enumeration(service_tags, stream, service_name, datacenter, node_name)
                            jsons = json.dumps(rezult)
                            urlz= 'http://consul.service.cdek.tech:8500/ui/#/'+datacenter+'/'+json+'/'+service_name+'/'+data['ref']+'/order-async-ec4/'+service_tags+'/'+node_name+'/configuration/edit'
                            print jsons

        return get_items(self, data)

    def srv(self, result, service_name):
        if self.DEFAULT_LOCATION in result:
            value = {
                self.DEFAULT_APP: {service_name: {
                    self.DEFAULT_ENVIRONMENT: {
                        self.DEFAULT_LOCATION: {
                            self.DEFAULT_NODE: result[self.DEFAULT_LOCATION][self.DEFAULT_NODE],
                        }}}}}
        elif self.DEFAULT_NODE in result:
            value = {
                self.DEFAULT_APP: {service_name: {
                    self.DEFAULT_ENVIRONMENT: {
                        self.DEFAULT_LOCATION: {
                            self.DEFAULT_NODE: result[self.DEFAULT_NODE],
                        }}}}}

        else:
            value = {
                self.DEFAULT_APP: {service_name: {
                    self.DEFAULT_ENVIRONMENT: {
                        self.DEFAULT_LOCATION: {
                            self.DEFAULT_NODE: result,
                        }}}}}
        return value




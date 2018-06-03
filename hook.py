# -*- coding: utf-8 -*-
from flask import Flask,request
from ruamel.yaml import YAML
import subprocess
import json
import requests
from ConsulApp import ConsulApplications

yaml = YAML()
yaml.allow_duplicate_keys = True
app = Flask(__name__)

consul= ConsulApplications()

@app.route("/index")
def test():
    return "Work!"

@app.route("/webhook", methods=['POST'])
def webhook():
    data = json.loads(request.data)
    print "New commit by: {}".format(data['commits'][0]['modified'])

    print "target branch: {}".format(data['ref'])
#    print "target repo: {}".format(data['commits'][0]['modified']

#mainblock
    work = data['commits'][0]['modified']
    works = work.__str__()

    if 'hive/applications' in works:
        master = consul.get(data)
        print master


#        git_pull = subprocess.call(("cd /home/demm/variables/ && git pull"), shell=True)
#        if git_pull == 0:
#            for path in path_list:
#                #вот эту гобшу явно можно сделать одной регуляркой, но регулярки для слабых
#                path_replace = path.replace("u'","").replace("'","").replace("[","").replace("]","").replace(" ","")
#                service_name_split = path.split('/')[-1:]
#                service_name = str(service_name_split).replace("u'","").replace("'","").replace("[","").replace("]","").replace(" ","").replace(".yml","").replace("'","").replace('"','')
#                #print service_name
#                #print path_replace
#                if 'hive/applications' in path_replace:
#                    stream = yaml.load(open('/home/demm/variables/%s' % path_replace))
#                    url = "http://192.168.0.126:8500/v1/catalog/service/" + service_name + ""
#                    #url = "http://192.168.0.126:8500/v1/catalog/service/api-pvz"
#                    data_json = requests.get(url).json()
#                    #if not data_json:
                     #   print 321
#                    for i in data_json:
#                        node_name = (i['Node'])
#                        z = (i['ServiceTags'])
#                        service_tags_split = str(z).split(',')[:-1]
#                        service_tags = str(service_tags_split).replace("u'", "").replace("'", "").replace("[",
#                                                                                                          "").replace( "]", "").replace('"', '')
#                        if service_tags in stream['application'][service_name]:
#                            default_environment = {}
#                            other_environment = {}
#                            default_environment.update(stream['application'][service_name]['default_environment'])
#                            other_environment.update(stream['application'][service_name][service_tags])
#                            merge_result = merge_environment(other_environment, default_environment)
#                            json_string = json.dumps(merge_result)
 #                           subprocess.call(("curl -X PUT -d " + json_string + "localhost:8500/" + service_name + "/" + service_tags +"/"+ node_name+"/"+service_name+""),
  #                                    shell=True)
   #                         print json_string
    #                    else:
     #                       default_environment = {}
      #                      default_environment.update(stream['application'][service_name]['default_environment'])
       #                     json_string_default = json.dumps(default_environment)
                            #subprocess.call((
                             #   "curl -X PUT -d " + json_string_default + "localhost:8500/" + service_name + "/" + service_tags + node_name + "/"+service_name+""),
                              #  shell=True)
        #
        #                  print json_string_default
        #print master
        return "ok"
    else:
        print '23132213'
        return 'ok'

#    else:
 #       return "Neok"
#main
#    if 'master' in data['ref']: #and 'hive/applications' in data['commits'][0]['modified']:
#        git_pull = subprocess.call(("cd /home/demm/variables/ && git pull"), shell=True)
#        if git_pull == 0:
#            for path in path_list:
#                #вот эту гобшу явно можно сделать одной регуляркой, но регулярки для слабых
#                path_replace = path.replace("u'","").replace("'","").replace("[","").replace("]","").replace(" ","")
#                service_name_split = path.split('/')[-1:]
#                service_name=str(service_name_split).replace("u'","").replace("'","").replace("[","").replace("]","").replace(" ","").replace(".yml","").replace("'","").replace('"','')
#                #print service_name
                #print path_replace
#                if 'hive/applications' in path_replace:
#                    stream = yaml.load(open('/home/demm/variables/%s' %path_replace))
#                    for k, v in dict_env.items():
#                        if k in stream['application'][service_name]:
#                            default_environment = {}
#                            other_environment= {}
#                            default_environment.update(stream['application'][service_name]['default_environment'])
#                            other_environment.update(stream['application'][service_name][k])
#                            merge_result= merge_environment(other_environment, default_environment)
#                            json_string = json.dumps(merge_result)
#                            subprocess.call(("curl -X PUT -d " + json_string + "localhost:8500/" + service_name + "/" + k + "/node_name"),
#                             #               shell=True)
#                            print json_string
                            #сделаем каунт для дефолтной среды, что бы не спамить дубль запросами в consul
                            #Не уверен, что эти данные вообще надо отправлять
                            #default_count=0
                            #default_count+=1
                            #if default_count <= 1:
                                #json_string_default=json.dump(default_environment)
                                #subprocess.call(("curl -X PUT -d "+json_string_default+"localhost:8500/" + service_name + "/default_environment/node_name"),
                                 #      shell=True)
                    #print stream
#        return 'OK'

#    else:
#        print 'tyt budet spam kydato'
#        return 'NEOK'

if __name__ == "__main__":
    app.run(host="172.16.24.91", port=8081, debug=True)

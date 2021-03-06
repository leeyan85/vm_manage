#!/usr/bin/python
from jira.client import JIRA
import json
import sys
jira=JIRA(basic_auth=("yangaofeng","ygf.1217"), server="http://jira.letv.cn/")

def get_InUse_ip(filename):
    ip_list=[]
    with open(filename) as f:
        hosts=f.readlines()
    for host in hosts:
        ip_list.append(u'%s'%host.strip("\n"))
    return ip_list




def delete_resource(ip):
    resources=jira.search_issues("project = SEERESOURCE AND VMIP ~ %s"%ip, maxResults=2)
    resource=resources[0]
    print ip,resource,resource.fields.customfield_15600
    resource.delete()



if __name__=="__main__":
    filename=sys.argv[1]
    ip_list=get_InUse_ip(filename)
    for ip in ip_list:
        delete_resource(ip)

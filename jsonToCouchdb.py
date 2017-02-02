#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import json
from user_define_classes import DnsServer
from user_define_classes import Server

server_dns = DnsServer('127.0.0.1', 5984)
server0 = Server('127.0.0.1', 5984)
#server1 = Server('192.168.37.5', 5984)
#server2 = Server('192.168.37.6', 5984)
servers = [
    server0
  #  server1,
   # server2
]
#server0.set_backup_server(server1)
#server1.set_backup_server(server2)
#server2.set_backup_server(server0)

rond = 0
for root, dirs, files in os.walk('news/', topdown=False):
    for name in files:
        print(os.path.join(root, name))
        one_file = open(os.path.join(root, name), 'r')
        array_news = json.loads(one_file.read(), "utf8")
        for news in array_news:
            _id = news['id']
            del news['id']
            if _id not in server_dns.get_dns_database():
                server = servers[rond]
                server.get_news_database()[_id] = news
                server_dns.get_dns_database()[_id] = {"address": server.get_server_address()}

                rond = (rond + 1) % len(servers)

            else:
                is_update_exist = False
                doc_place = server_dns.get_dns_database()[_id]
                address = doc_place['address']
                news_inDb = None

                db = None
                for server in servers:
                    if server.is_this_server(address) and server.is_available():
                        db = server.get_news_database()
                        break

                news_inDb = db[_id]
                for key in news.keys():
                    if news[key] != news_inDb.get(key):
                        news_inDb[key] = news[key]
                        is_update_exist = True

                if is_update_exist:
                    db[news_inDb.id] = news_inDb

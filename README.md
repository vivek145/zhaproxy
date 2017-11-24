# ZHaproxy

This template works on CentOS 7 and Zabbix 3.4.

The python script is executing as a service, listening on http://127.0.0.1:8081, the  zabbix-agent uses to discover all frontends, backends and servers backends.

### Requirements
 - To haproxy(_Tested on version 1.5_):
   -   stats socket enabled
 - To python3
   - bottle==0.12.13
   - [haproxyadmin==0.2.1](http://haproxyadmin.readthedocs.io/en/latest/)
 - Zabbix-agent (_Tested on version 3.4_)
 - Systemd

### Installation
- Create the directory /etc/zabbix/scripts
- Copy the file zhaproxy.py to /etc/zabbix/scripts
```console
# mkdir -p /etc/zabbix/scripts
# cp zhaproxy.py /etc/zabbix/scripts
# chmod +x /etc/zabbix/scripts
# chown -R zabbix: /etc/zabbix/scripts
```
- Copy the file zhaproxy.conf to /etc/zabbix/zabbix_agentd.d/
- Copy the file zabbix-haproxy.service to /etc/systemd/system/ Copy the file zabbix-haproxy.service to /etc/systemd/system/, after you have enabled and started the service
```console
# systemctl enable zabbix-haproxy ; systemctl start zabbix-haproxy
```



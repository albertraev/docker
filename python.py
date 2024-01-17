from pyzabbix import ZabbixAPI

ZABBIX_SERVER = "https://zabbix.from.sh"

zapi = ZabbixAPI(ZABBIX_SERVER)

zapi.login("api_username", "api_password")

triggers = zapi.trigger.get(
    only_true=1,
    skipDependent=1,
    monitored=1,
    active=1,
    output="extend",
    expandDescription=1,
    selectHosts=["host"],
)
unack_triggers = zapi.trigger.get(only_true=1,
                                  skipDependent=1,
                                  monitored=1,
                                  active=1,
                                  output='extend',
                                  expandDescription=1,
                                  selectHosts=['host'],
                                  withLastEventUnacknowledged=1,
                                  )
unack_trigger_ids = [t['triggerid'] for t in unack_triggers]
for t in triggers:
    t['unacknowledged'] = True if t['triggerid'] in unack_trigger_ids \
        else False

# Print a list containing only "tripped" triggers
for t in triggers:
    if int(t['value']) == 1:
        print("{0} - {1} {2}".format(t['triggerid'],t['hosts'][0]['host'],
                                     t['description'],
                                     '(Unack)' if t['unacknowledged'] else '')
              )
	print t

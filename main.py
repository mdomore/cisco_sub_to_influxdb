import netsnmp
import json

from influxdb import InfluxDBClient

with open("config.json") as json_data_file:
    data = json.load(json_data_file)

result = list()
key = data['snmp']['community']
OID_1 = '.1.3.6.1.4.1.9.9.786.1.2.1.1.6.1.1'
OID_22 = '.1.3.6.1.4.1.9.9.786.1.1.1.1.22'
OID_23 = '.1.3.6.1.4.1.9.9.786.1.1.1.1.23'
OID_24 = '.1.3.6.1.4.1.9.9.786.1.1.1.1.24'

client = InfluxDBClient(host=data['influx']['host'], port=data['influx']['port'])
client.create_database('ciscoDetailSub')
client.switch_database('ciscoDetailSub')


def get_total_subs():
    """
    Get Total subs for each host

    OID : .1.3.6.1.4.1.9.9.786.1.2.1.1.6.1.1
    This object indicates the current number of subscriber session
    within the 'scope of aggregation' that have been authenticated.

    This function collect the total subscribers on each router.
    """
    for h in data['hosts']:
        ip = data['hosts'][h]['ip']
        var = netsnmp.Varbind(OID_1)
        vars_list = netsnmp.VarList(var)
        session = netsnmp.Session(DestHost=ip, Version=2, Community=key)
        session.UseLongNames = 1
        sub_number = session.walk(vars_list)
        if sub_number:
            data['hosts'][h]['nb_sub'] = int(sub_number[0].decode("utf-8"))
        else:
            data['hosts'][h]['nb_sub'] = 0


def get_detailed_subs():
    """
    Get detailed subs

    OID : .1.3.6.1.4.1.9.9.786.1.1.1.1.22
    This object indicates the NAS port-identifier identifying the
    port on the NAS providing access to the subscriber.

    OID : .1.3.6.1.4.1.9.9.786.1.1.1.1.23
    This object indicates the domain associated with the
    subscriber.

    OID : .1.3.6.1.4.1.9.9.786.1.1.1.1.24
    This object indicates the username identifying the subscriber.

    This function collect information (NAS port, domain and username) about subscribers.
    """

    for h in data['hosts']:
        ip = data['hosts'][h]['ip']
        var_oid_22 = netsnmp.Varbind(OID_22)
        var_oid_23 = netsnmp.Varbind(OID_23)
        var_oid_24 = netsnmp.Varbind(OID_24)
        vars_list = netsnmp.VarList(var_oid_22, var_oid_23, var_oid_24)
        session = netsnmp.Session(DestHost=ip, Version=2, Community=key)
        session.UseLongNames = 1
        for i in range(data['hosts'][h]['nb_sub']):
            reply = session.getnext(vars_list)
            result.append(
                {'vlan': (int(reply[0].decode("utf-8").split('/')[-1].split('.')[0])),
                 'domain': (reply[1].decode("utf-8").split('.', 1)[1]),
                 'user': (reply[2].decode("utf-8"))}
            )


def count_subs_by_type():
    """
    This function count how many subs of each type is connected.
    Result is push in data variable
    """
    for item in result:
        vlan = item['vlan']
        domain = item['domain']
        for t in data['influx']['type']:
            c_vlan = data['influx']['type'][t]['vlan']
            c_domain = data['influx']['type'][t]['domain']
            c_no_vlan = str(data['influx']['type'][t]['novlan']).split(',')
            if vlan == c_vlan:
                data['influx']['type'][t]['nb_sub'] += 1
            elif c_domain == domain and c_vlan == 0 and str(vlan) not in c_no_vlan:
                data['influx']['type'][t]['nb_sub'] += 1


def write_totals_to_influxdb():
    """
    Writing total connections for each hosts
    """
    for h in data['hosts']:
        json_body = [
            {
                "measurement": "subscribers",
                "tags": {
                    "type": 'sub-' + data['hosts'][h]['ip']
                },
                "fields": {
                    "value": data['hosts'][h]['nb_sub']
                }
            }
        ]
        client.write_points(json_body)


def write_subs_to_influxdb():
    """
    Writing values in influxdb
    """
    for t in data['influx']['type']:
        json_body = [
            {
                "measurement": "subscribers",
                "tags": {
                    "type": t
                },
                "fields": {
                    "value": data['influx']['type'][t]['nb_sub']
                }
            }
        ]
        client.write_points(json_body)


if __name__ == "__main__":
    get_total_subs()
    get_detailed_subs()
    count_subs_by_type()
    write_totals_to_influxdb()
    write_subs_to_influxdb()

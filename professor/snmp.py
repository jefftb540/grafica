from pysnmp import hlapi
from models import Contagem
targets = ['192.168.191.23', '192.168.191.20', '192.168.191.15', '192.168.191.21', '192.168.191.18', '192.168.191.17', '192.168.191.5', '192.168.191.19', '192.168.191.16', '192.168.191.23'] 
oid = '.1.3.6.1.2.1.43.10.2.1.4.1.1'
def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types

def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value


def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
            	print 'impressora nao respondeu'
                #raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result



def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_object_types(oids)
    )
    return fetch(handler, 1)[0]

def getTotalGeral():
	total = 0  
	for target in targets:
		total += get(target,[oid], hlapi.CommunityData('public'))[0]

	totalGeral = Contagem.objects.latest('contagem') - total
	return totalGeral




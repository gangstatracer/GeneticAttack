import ConfigParser

import attack_engine


ipMap = {}
tcpMap = {}
icmpMap = {}
attack_constants = {}
url_to_download = ""
_infinity_ = 100000.0

def reload_conf():
    global config, ipMap, tcpMap, icmpMap, attack_constants, url_to_download
    config = ConfigParser.ConfigParser()
    config.read("defaults.ini")
    ipMap = config_section_map("ip")
    tcpMap = config_section_map("tcp")
    icmpMap = config_section_map("icmp")
    attack_max = config_section_map("attack_params_max")
    url_to_download = config_section_map("url")["address"]
    duration_bounds = map(int, attack_max["duration"].split(' '))
    attack_constants = {
        0: (attack_engine.AttackType.UDP, attack_engine.AttackType.TCP, attack_engine.AttackType.ICMP),  # attack type
        1: xrange(duration_bounds[0], duration_bounds[1]),  # duration
        2: xrange(int(attack_max["interval"])),  # interval
        3: (True, False),  # xrange(2),  # random flags
        4: (True, False),  #xrange(2),
        5: (True, False),  #xrange(2),
        6: attack_engine.get_random_ip,  # source ip
        7: attack_engine.get_random_port,  # source port
        8: attack_engine.get_random_port,  # destination port
        9: xrange(int(attack_max["data_length"]))  # data length
    }


def config_section_map(section):
    dictionary = {}
    options = config.options(section)
    for option in options:
        try:
            dictionary[option] = config.get(section, option)
            if dictionary[option] == -1:
                print "skip: %s" % option
        except:
            print "exception on %s!" % option
            dictionary[option] = None
    return dictionary

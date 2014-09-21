import ConfigParser

import attack_engine


ipMap = {}
tcpMap = {}
icmpMap = {}
attack_constants = {}
url_to_download = ""


def reload_conf():
    global config, ipMap, tcpMap, icmpMap, attack_constants, url_to_download
    config = ConfigParser.ConfigParser()
    config.read("defaults.ini")
    ipMap = config_section_map("ip")
    tcpMap = config_section_map("tcp")
    icmpMap = config_section_map("icmp")
    attack_max = config_section_map("attack_params_max")
    url_to_download = config_section_map("url")["address"]
    attack_constants = {
        0: (attack_engine.AttackType.UDP, attack_engine.AttackType.TCP, attack_engine.AttackType.ICMP),  # attack type
        1: xrange(int(attack_max["duration"])),  # duration
        2: xrange(int(attack_max["interval"])),  # interval
        3: xrange(1),  # random flags
        4: xrange(1),
        5: xrange(1),
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

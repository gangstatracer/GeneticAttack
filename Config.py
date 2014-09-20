import ConfigParser


ipMap = {}
tcpMap = {}
icmpMap = {}


def reload_conf():
    global config, ipMap, tcpMap, icmpMap
    config = ConfigParser.ConfigParser()
    config.read("defaults.ini")
    ipMap = config_section_map("ip")
    tcpMap = config_section_map("tcp")
    icmpMap = config_section_map("icmp")


def config_section_map(section):
    dict = {}
    options = config.options(section)
    for option in options:
        try:
            dict[option] = config.get(section, option)
            if dict[option] == -1:
                print "skip: %s" % option
        except:
            print "exception on %s!" % option
            dict[option] = None
    return dict

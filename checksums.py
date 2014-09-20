def icmp_checksum(source_string):
    sum = 0
    count_to = (len(source_string) / 2) * 2
    count = 0
    while count < count_to:
        this_val = ord(source_string[count + 1]) * 256 + ord(source_string[count])
        sum += this_val
        sum &= 0xffffffff
        count += 2
    if count_to < len(source_string):
        sum += ord(source_string[len(source_string) - 1])
        sum &= 0xffffffff
    sum = (sum >> 16) + (sum & 0xffff)
    sum += sum >> 16
    answer = ~sum
    answer &= 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def tcp_checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = (ord(msg[i]) << 8) + (ord(msg[i + 1]) )
        s += w

    s = (s >> 16) + (s & 0xffff);
    s = ~s & 0xffff
    return s

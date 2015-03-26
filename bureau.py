# XXX Need to get bridge descriptors for 24 hours. Not just one file.


from stem.descriptor import parse_file
import sys

import grapher

class Bridges(object):
    def __init__(self):
        self.bridges = []

    def add_bridge(self, fingerprint, read_history, write_history):
        bridge = Bridge(fingerprint, read_history, write_history)

        # Don't accept bridges if they don't report a full day of measurements.
        if bridge.get_interval_time() < 24:
            print "[*] Incomplete interval period. Ignoring."
            return

        if self.bridge_is_duplicate(fingerprint):
            return

        self.bridges.append(bridge)

    def bridge_is_duplicate(self, fingerprint):
        """
        Do we already have a bridge with this fingerprint?
        XXX worst performance ever
        """
        for bridge in self.bridges:
            if fingerprint == bridge.fingerprint:
                return True
        return False

    def report_statistics(self):
        """Do the thing!!!"""

        for bridge in self.bridges:
            print "\t%s: %d" % (bridge.fingerprint, bridge.get_total_read())
            bridge.describe_bw_scarcity()

        # XXX Calculate period length

        self.report_read_history_distr()

    def report_read_history_distr(self):
        """Report various statistics about the read history distribution."""


        # Dictionary of bridg fingerprint to total read history
        read_histories = {}

        # Populate dictionary with total read history for each bridge.
        for bridge in self.bridges:
            read_histories[bridge.fingerprint] = bridge.get_total_read() / pow(10,6) # bytes to megabytes

        # Get average of all read histories
        total_sum = sum(read_histories.values())
        average = float(total_sum) / len(read_histories.values())

        # Get median of all read histories
        median = read_histories.values()[len(read_histories.values())/2]

        # Get min
        minimum_read_history = min(read_histories.values())
        minimum_bridge = read_histories.keys()[read_histories.values().index(minimum_read_history)] # XXX oh wow terrible!

        # and max
        maximum_read_history = max(read_histories.values())
        maximum_bridge = read_histories.keys()[read_histories.values().index(maximum_read_history)]

        # Report out
        print "\t\tGot %d bridges" % (len(read_histories))
        print "\t\tAverage read history sum: %d" % average
        print "\t\tMedian read history sum: %d" % median
        print "\t\tMin read history sum: %d (by %s)" % (minimum_read_history, minimum_bridge)
        print "\t\tMax read history sum: %d (by %s)" % (maximum_read_history, maximum_bridge)

#        print sorted(read_histories.values())

        grapher.graph_read_history(read_histories.values())

    def is_duplicate_bridge(self):
        pass

class Bridge(object):
    def __init__(self, fingerprint, read_history, write_history):
        self.fingerprint = fingerprint
        self.read_history = read_history
        self.write_history = write_history

    def describe_bw_scarcity(self):
        if sum(self.read_history) == 0:
            print "\t\tunused bridge"

#        zeroes_n = self.read_history.count(0)
#        total_observations = len(self.read_history)
#        return "with %d zeroes out of %d observations" % (zeroes_n, total_observations)


    def get_interval_time(self):
        """
        Return the number of hours that the bridge has been collecting
        statistics for. Bridges publish a descriptor every day, which
        means that 24 hours covers the whole previous day
        """

        # Each element of read_history represents a 15 minute interval.
        # There are four 15-minute intervals in an hour
        return len(self.read_history) / 4


    def get_total_read(self):
        """Get sum of read history bytes."""
        return sum(self.read_history)

def usage():
    print "bureau.py <filename with bridge extrainfo descs>"

def main():
    bridges = Bridges()

    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    for desc in parse_file(sys.argv[1], "bridge-extra-info 1.2"):
        if not desc.read_history_values: # XXX is this a bug? Why some descs don't have read_history_values?
            print "[!] %s %s" % (desc.fingerprint, desc.read_history_values)
            continue

        bridges.add_bridge(desc.fingerprint, desc.read_history_values, desc.write_history_values)

    bridges.report_statistics()

if __name__ == "__main__":
    main()


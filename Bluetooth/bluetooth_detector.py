import time
import requests
import bluetooth

previous_addr = []

while True:
    print "Start scanning..."
    try:
        nearby_device = bluetooth.discover_devices(duration=4, lookup_names=True, flush_cache=True, lookup_class=False)
        for addr, name in nearby_device:
            try:
                print "\t%s - %s" % (addr, name)

                if len(name) == 0:
                    continue
                # weird, don't know the meaning, what's the url for.
                if addr in previous_addr:
                    url = "http://localhost:3000/bluetooth?bluetooth_id=" + addr
                    req = requests.get(url)
                    res = req.content
                    previous_addr.remove(addr)
                    print res
                    if res[:7].decode("utf-8") == "success":
                        time.sleep(5)
                        break
                    continue
                previous_addr.append(addr)
            except UnicodeEncodeError:
                print "\t%s - %s" % (addr, name.encode("utf-8", 'replace'))

        if len(previous_addr) > 10:
            previous_addr.pop(0)
    except Exception, e:
        print "Error:\n",e.message



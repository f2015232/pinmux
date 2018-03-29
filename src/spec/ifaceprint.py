#!/usr/bin/env python

from copy import deepcopy


def display(pins):
    print "| Pin | Mux0        | Mux1        | Mux2        | Mux3        |"
    print "| --- | ----------- | ----------- | ----------- | ----------- |"
    pinidx = sorted(pins.keys())
    for pin in pinidx:
        pdata = pins.get(pin)
        res = '| %3d |' % pin
        for mux in range(4):
            if mux not in pdata:
                res += "             |"
                continue
            name, bank = pdata[mux]
            res += " %s %-9s |" % (bank, name)
        print res


def fnsplit(f):
    a = ''
    n = 0
    if not f.startswith('FB_'):
        f2 = f.split('_')
        if len(f2) == 2:
            if f2[1].isdigit():
                return f2[0], int(f2[1])
            return f2[0], f2[1]
    #print f
    while f and not f[0].isdigit():
        a += f[0]
        f = f[1:]
    return a, int(f) if f else None


def fnsort(f1, f2):
    a1, n1 = fnsplit(f1)
    a2, n2 = fnsplit(f2)
    x = cmp(a1, a2)
    if x != 0:
        return x
    return cmp(n1, n2)


def find_fn(fname, names):
    for n in names:
        if fname.startswith(n):
            return n


def display_fns(bankspec, pins, function_names):
    fn_names = function_names.keys()
    fns = {}
    for (pin, pdata) in pins.items():
        for mux in range(1, 4):  # skip GPIO for now
            if mux not in pdata:
                continue
            name, bank = pdata[mux]
            assert name is not None, str(bank)
            if name not in fns:
                fns[name] = []
            fns[name].append((pin - bankspec[bank], mux, bank))

    fnidx = fns.keys()
    fnidx.sort(fnsort)
    current_fn = None
    for fname in fnidx:
        fnbase = find_fn(fname, fn_names)
        #print "name", fname, fnbase
        if fnbase != current_fn:
            if current_fn is not None:
                print
            print "## %s" % fnbase
            print
            print function_names[fnbase]
            print
            current_fn = fnbase
        print "* %-9s :" % fname,
        for (pin, mux, bank) in fns[fname]:
            print "%s%d/%d" % (bank, pin, mux),
        print

    return fns


def check_functions(title, bankspec, fns, pins, required, eint, pwm,
                    descriptions=None):
    fns = deepcopy(fns)
    pins = deepcopy(pins)
    if descriptions is None:
        descriptions = {}

    print "# Pinmap for %s" % title
    print

    for name in required:
        print "## %s" % name
        print
        if descriptions and name in descriptions:
            print descriptions[name]
            print

        name = name.split(':')
        if len(name) == 2:
            findbank = name[0][0]
            findmux = int(name[0][1:])
            name = name[1]
        else:
            name = name[0]
            findbank = None
            findmux = None
        name = name.split('/')
        if len(name) == 2:
            count = int(name[1])
        else:
            count = 100000
        name = name[0]
        found = set()
        fnidx = fns.keys()
        # fnidx.sort(fnsort)
        pinfound = {}
        for fname in fnidx:
            if not fname.startswith(name):
                continue
            for pin, mux, bank in fns[fname]:
                if findbank is not None:
                    if findbank != bank:
                        continue
                    if findmux != mux:
                        continue
                pin_ = pin + bankspec[bank]
                if pin_ in pins:
                    pinfound[pin_] = (fname, pin_, bank, pin, mux)

        pinidx = sorted(pinfound.keys())

        for pin_ in pinidx:
            fname, pin_, bank, pin, mux = pinfound[pin_]
            if fname in found:
                continue
            found.add(fname)
            if len(found) > count:
                continue
            del pins[pin_]
            print "* %s %d %s%d/%d" % (fname, pin_, bank, pin, mux)

        print

    # gpios
    gpios = []
    for name in descriptions.keys():
        if not name.startswith('GPIO'):
            continue
        if name == 'GPIO':
            continue
        gpios.append(name)
    gpios.sort()

    if gpios:
        print "## GPIO"
        print

        for fname in gpios:
            if fname in found:
                continue
            desc = ''
            if descriptions and fname in descriptions:
                desc = ': %s' % descriptions[fname]
            bank = fname[4]
            pin = int(fname[7:])
            pin_ = pin + bankspec[bank]
            if pin_ not in pins:
                continue
            del pins[pin_]
            found.add(fname)
            print "* %-8s %d %s%-2d %s" % (fname, pin_, bank, pin, desc)
        print

    if eint:
        display_group(bankspec, "EINT", eint, fns, pins, descriptions)
    if pwm:
        display_group(bankspec, "PWM", pwm, fns, pins, descriptions)

    print "## Unused Pinouts (spare as GPIO) for '%s'" % title
    print
    if descriptions and 'GPIO' in descriptions:
        print descriptions['GPIO']
        print
    display(pins)
    print

    return pins  # unused


def display_group(bankspec, title, todisplay, fns, pins, descriptions):
    print "## %s" % title
    print

    found = set()
    for fname in todisplay:
        desc = ''
        if descriptions and fname in descriptions:
            desc = ': %s' % descriptions[fname]
        fname = fname.split(':')
        if len(fname) == 2:
            findbank = fname[0][0]
            findmux = int(fname[0][1:])
            fname = fname[1]
        else:
            fname = fname[0]
            findbank = None
            findmux = None
        for (pin, mux, bank) in fns[fname]:
            if findbank is not None:
                if findbank != bank:
                    continue
                if findmux != mux:
                    continue
            if fname in found:
                continue
            pin_ = pin + bankspec[bank]
            if pin_ not in pins:
                continue
            del pins[pin_]
            found.add(fname)
            print "* %s %d %s%d/%d %s" % (fname, pin_, bank, pin, mux, desc)
    print


def display_fixed(fixed, offs):

    fkeys = sorted(fixed.keys())
    pin_ = offs
    res = []
    for pin, k in enumerate(fkeys):
        print "## %s" % k
        print
        prevname = ''
        linecount = 0
        for name in fixed[k]:
            if linecount == 4:
                linecount = 0
                print
            if prevname[:2] == name[:2] and linecount != 0:
                print name,
                linecount += 1
            else:
                if linecount != 0:
                    print
                print "* %d: %d %s" % (pin_, pin, name),
                linecount = 1
                res.append((pin_, name))

            prevname = name
            pin_ += 1
        if linecount != 0:
            print
        print

    return res

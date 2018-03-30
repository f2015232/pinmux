#!/usr/bin/env python

from spec.pinfunctions import pinspec
from copy import deepcopy

def namesuffix(name, suffix, namelist):
    names = []
    for n in namelist:
        if n:
            names.append("%s%s_%s" % (name, suffix, n))
        else:
            names.append("%s_%s" % (name, suffix))
    return names


class PinGen(object):
    def __init__(self, pinouts, fname, pinfn, bankspec):
        self.pinouts = pinouts
        self.bankspec = bankspec
        self.pinfn = pinfn
        self.fname = fname

    def __call__(self, suffix, offs, bank, mux,
                 start=None, limit=None, spec=None, origsuffix=None):
        pingroup = self.pinfn(suffix, bank)
        if isinstance(pingroup, tuple):
            prefix, pingroup = pingroup
        else:
            prefix = self.fname
        if start and limit:
            limit = start + limit
        pingroup = pingroup[start:limit]
        pins = Pins(prefix, pingroup, self.bankspec,
                    suffix, offs, bank, mux,
                    spec, origsuffix=suffix)
        self.pinouts.pinmerge(pins)

# pinouts class

class Pinouts(object):
    def __init__(self, bankspec):
        self.bankspec = bankspec
        self.pins = {}
        self.fnspec = {}
        for fname, pinfn in pinspec:
            if isinstance(pinfn, tuple):
                name, pinfn = pinfn
            else:
                name = pinfn.__name__
            setattr(self, name, PinGen(self, fname, pinfn, self.bankspec))

    def __contains__(self, k):
        return k in self.pins

    def has_key(self, k):
        return k in self.pins

    def add_spec(self, k, v):
        self.fnspec[k] = v

    def update(self, pinidx, v):
        if pinidx not in self.pins:
            self.pins[pinidx] = v
        else:
            for k in v:
                assert k not in self.pins[pinidx], \
                    "pin %d position %d already taken\n%s\n%s" % \
                        (pinidx, k, str(v), self.pins[pinidx])
            self.pins[pinidx].update(v)

    def keys(self):
        return self.pins.keys()

    def items(self):
        return self.pins.items()

    def get(self, k):
        return self.pins[k]

    def __len__(self):
        return len(self.pins)

    def __delitem__(self, k):
        del self.pins[k]

    def __getitem__(self, k):
        return self.pins[k]

    def pinmerge(self, fn):
        # hack, store the function specs in the pins dict
        fname = fn.fname
        suffix = fn.origsuffix
        bank = fn.bank

        if not hasattr(self, 'fnspec'):
            self.fnspec = pins
        if fname == 'GPIO':
            fname = fname + bank
        assert 'EINT' not in self
        if fname not in self.fnspec:
            self.add_spec(fname, {})
        if suffix or fname == 'EINT' or fname == 'PWM':
            specname = fname + suffix
        else:
            specname = fname
        #print "fname bank specname suffix ", fname, bank, specname, repr(
        #    suffix)
        if specname in self.fnspec[fname]:
            # ok so some declarations may bring in different
            # names at different stages (EINT, PWM, flexbus1/2)
            # so we have to merge the names in.  main thing is
            # the pingroup
            tomerge = self.fnspec[fname][specname]
            for p in fn.pingroup:
                if p not in tomerge.pingroup:
                    tomerge.pingroup.append(p)
            tomerge.pins.update(fn.pins)
            tomerge.fntype.update(fn.fntype)
        else:
            self.fnspec[fname][specname] = deepcopy(fn)

        # merge actual pins
        for (pinidx, v) in fn.pins.items():
            self.update(pinidx, v)


class Pins(object):

    def __init__(self, fname, pingroup, bankspec, suffix, offs, bank, mux,
                 spec=None, limit=None, origsuffix=None):

        # function type can be in, out or inout, represented by - + *
        # strip function type out of each pin name
        self.fntype = {}
        for i in range(len(pingroup)):
            pname = pingroup[i]
            if not pname:
                continue
            fntype = pname[-1]
            if fntype not in '+-*':
                continue
            pname = pname[:-1]
            fntype = {'-': 'in', '+': 'out', '*': 'inout'}[fntype]
            self.fntype[pname] = fntype
            pingroup[i] = pname

        self.fname = fname
        self.pingroup = pingroup
        self.bankspec = bankspec
        self.suffix = suffix
        self.origsuffix = origsuffix or suffix
        self.bank = bank
        self.mux = mux

        # create consistent name suffixes
        pingroup = namesuffix(fname, suffix, pingroup)
        suffix = ''  # hack

        res = {}
        names = {}
        idx = 0
        for name in pingroup[:limit]:
            if suffix and name:
                name_ = "%s_%s" % (name, suffix)
            else:
                name_ = name
            if spec and name in spec:
                continue
            pin = {mux: (name_, bank)}
            offs_bank, offs_ = offs
            idx_ = offs_ + idx
            idx += 1
            idx_ += bankspec[bank]
            res[idx_] = pin
            names[name] = idx_
        for name in pingroup:
            if suffix and name:
                name_ = "%s_%s" % (name, suffix)
            else:
                name_ = name
            if not spec:
                continue
            if name not in spec:
                continue
            idx_, mux_, bank_ = spec[name]
            idx_ = names[idx_]
            pin = {mux_: (name_, bank_)}
            if idx_ in res:
                res[idx_].update(pin)
            else:
                res[idx_] = pin

        self.pins = res

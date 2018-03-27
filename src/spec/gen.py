import os
import os.path
from spec.interfaces import Pinouts

def specgen(pth, pinouts, bankspec, fixedpins):
    """ generates a specification of pinouts (tsv files)
        for reading in by pinmux
    """
    pth = pth or ''
    #print bankspec.keys()
    #print pinouts.keys()
    #print fixedpins.keys()
    if not os.path.exists(pth):
        os.makedirs(pth)
    with open(os.path.join(pth, 'interfaces.txt'), 'w') as f:
        for k in pinouts.fnspec.keys():
            s = pinouts.fnspec[k]
            f.write("%s\t%d\n" % (k.lower(), len(s)))
            s0 = s[s.keys()[0]] # hack, take first
            with open(os.path.join(pth, '%s.txt' % k.lower()), 'w') as g:
                if len(s0.pingroup) == 1: # only one function, grouped higher up
                    for ks in s.keys():  # grouped by interface
                        k = "%s_%s" % (s[ks].fname, s[ks].suffix)
                        k_ = k.lower()
                        g.write("%s\t%s\n" % (k_, fntype))
                else:
                    for pinname in s0.pingroup:
                        fntype = s0.fntype.get(pinname, 'inout')
                        k_ = k.lower()
                        pn = pinname.lower()
                        g.write("%s_%s\t%s\n" % (k_, pn, fntype))

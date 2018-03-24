import os
import os.path

def specgen(pth, pinouts, bankspec, fixedpins):
    """ generates a specification of pinouts (tsv files)
        for reading in by pinmux
    """
    pth = pth or ''
    print bankspec.keys()
    print pinouts.keys()
    print fixedpins.keys()
    if not os.path.exists(pth):
        os.makedirs(pth)
    with open(os.path.join(pth, 'interfaces.txt'), 'w') as f:
        for k in pinouts.fnspec.keys():
            f.write("%s\t%d\n" % (k.lower(), len(pinouts.fnspec[k])))

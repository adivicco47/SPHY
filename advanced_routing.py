# Advanced routing that is used for reservoirs or lakes
print 'Advanced routing module for lakes and reservoirs imported'

#-Function to rout the specific runoff
def ROUT(pcr, fracq, flowdir, storact):
    S = pcr.accufractionstate(flowdir, storact, fracq)
    Q = pcr.accufractionflux(flowdir, storact, fracq)
    #-Convert Q to m3/s
    Q = Q / (24 * 3600)
    return S, Q
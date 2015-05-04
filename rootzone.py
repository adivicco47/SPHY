#-Function to calculate rootzone runoff
def RootRunoff(pcr, rainfrac, rootwater, rootsat, rootfield, rain, rootksat):
    #-infiltration capacity, scaled based on rootwater content and ksat
    Infil_cap = rootksat * pcr.max(pcr.min(1, 1 - (rootwater - rootfield)/(rootsat - rootfield)), 0)
    #-infiltration
    Infil = pcr.max(0, pcr.min(rain, Infil_cap, rootsat - rootwater))
    #-Runoff
    rootrunoff = pcr.ifthenelse(rainfrac > 0, rain - Infil, 0)
    #-Updated rootwater content
    rootwater = pcr.ifthenelse(rainfrac > 0, rootwater + Infil, rootwater)
    return rootrunoff, rootwater

#-Function to calculate rootzone drainage
def RootDrainage(pcr, rootwater, rootdrain, rootfield, rootsat, drainvel, rootTT):
    rootexcess = pcr.max(rootwater - rootfield)
    rootexcessfrac = rootexcess / (rootsat - rootfield)
    rootlat = rootexcessfrac * drainvel
    rootdrainage = pcr.max(pcr.min(rootwater, (rootlat + rootdrain) * (1 - pcr.exp(-1 / rootTT))), 0)
    return rootdrainage

#-Function to calculate rootzone percolation
def RootPercolation(pcr, rootwater, subwater, rootfield, rootTT, subsat):
    rootexcess = pcr.max(rootwater - rootfield, 0)
    rootperc = rootexcess * (1 - pcr.exp(-1 / rootTT))
    rootperc = pcr.ifthenelse(subwater >= subsat, 0, pcr.min(subsat - subwater, rootperc))
    rootperc = pcr.max(pcr.min(rootperc, rootwater), 0)
    return rootperc
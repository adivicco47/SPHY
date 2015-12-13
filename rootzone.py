#-Function to calculate rootzone runoff
def RootRunoff(self, pcr, rainfrac, rain):
    #-At the moment, only apply reduced infiltration rate if sediment module is used.
    if self.SedFLAG == 1:
        #-infiltration capacity, scaled based on rootwater content and ksat
        Infil_cap = self.RootKsat * (pcr.max(pcr.min(1, 1 - (self.RootWater - \
            self.RootDry)/(self.RootSat - self.RootDry)), 0))**self.Infil_alpha
    else: #-assume infiltration capacity to be equal to saturated hydraulic conductivity
        Infil_cap = self.RootKsat
    self.report(Infil_cap, self.outpath + 'InfCap')
    #-infiltration
    Infil = pcr.max(0, pcr.min(rain, Infil_cap, self.RootSat - self.RootWater))
    self.report(Infil, self.outpath + 'Infil')
    #-Runoff
    rootrunoff = pcr.ifthenelse(rainfrac > 0, rain - Infil, 0)
    #-Updated rootwater content
    self.RootWater = pcr.ifthenelse(rainfrac > 0, self.RootWater + Infil, self.RootWater)
    return rootrunoff, self.RootWater

#-Function to calculate rootzone drainage
def RootDrainage(pcr, rootwater, rootdrain, rootfield, rootsat, drainvel, rootTT):
    rootexcess = pcr.max(rootwater - rootfield, 0)
    rootexcessfrac = rootexcess / (rootsat - rootfield)
    rootlat = rootexcessfrac * drainvel
    rootdrainage = pcr.max(pcr.min(rootwater, rootlat * (1-pcr.exp(-1/rootTT)) + rootdrain * pcr.exp(-1/rootTT)), 0)
    return rootdrainage

#-Function to calculate rootzone percolation
def RootPercolation(pcr, rootwater, subwater, rootfield, rootTT, subsat):
    rootexcess = pcr.max(rootwater - rootfield, 0)
    rootperc = rootexcess * (1 - pcr.exp(-1 / rootTT))
    rootperc = pcr.ifthenelse(subwater >= subsat, 0, pcr.min(subsat - subwater, rootperc))
    rootperc = pcr.max(pcr.min(rootperc, rootwater), 0)
    return rootperc

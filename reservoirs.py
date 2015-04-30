print 'Reservoir module imported'

#-Advanced reservoir     
def QFracAdv(self, pcr):
    DayNo = self.timecalc.julian(self)[0]
    #-determine if it is flood or dry season
    S1 = pcr.ifthenelse(self.ResFlStart < self.ResFlEnd, pcr.ifthenelse(DayNo>=self.ResFlStart, pcr.ifthenelse(DayNo<=self.ResFlEnd, pcr.boolean(1), pcr.boolean(0)), pcr.boolean(0)),\
                        pcr.ifthenelse(DayNo>=self.ResFlEnd, pcr.ifthenelse(DayNo>=self.ResFlStart, pcr.boolean(1), pcr.boolean(0)), pcr.ifthenelse(DayNo<=self.ResFlEnd, \
                        pcr.ifthenelse(DayNo<=self.ResFlStart, pcr.boolean(1), pcr.boolean(0)), pcr.boolean(0))))

    S_avail = pcr.max(self.StorAct - self.ResPVOL, 0)
    Q = pcr.max(pcr.ifthenelse(S1, self.ResMaxFl * S_avail / (self.ResEVOL - self.ResPVOL),\
        self.ResDemFl * S_avail / (self.ResEVOL - self.ResPVOL)), self.StorAct - self.ResEVOL)
    Qfrac = Q / self.StorAct
    return Qfrac

#-Simple reservoir    
def QFracSimple(self, pcr):
    Q = pcr.max(self.ResKr * self.StorAct * (self.StorAct / self.ResSmax)**1.5, self.StorAct - self.ResSmax)
    Qfrac = Q / self.StorAct
    return Qfrac
    
#-Calculates the fraction to release, depending on the type of reservoir (simple or advanced)    
def QFrac(self, pcr):
    if self.ResSimple and self.ResAdvanced:
        Qfrac = pcr.ifthenelse(self.ResFunc==1, QFracSimple(self, pcr), pcr.ifthenelse(self.ResFunc==2,\
        QFracAdv(self, pcr), 1 - self.kx))
    elif self.ResSimple:
        Qfrac = pcr.ifthenelse(self.ResFunc==1, QFracSimple(self, pcr), 1 - self.kx)
    else:
        Qfrac = pcr.ifthenelse(self.ResFunc==2, QFracAdv(self, pcr), 1 - self.kx)
    Qfrac = pcr.max(pcr.min(Qfrac, 1), 0)
    return Qfrac

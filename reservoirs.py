# The Spatial Processes in HYdrology (SPHY) model:
# A spatially distributed hydrological model that calculates soil-water and
# cryosphere processes on a cell-by-cell basis.
#
# Copyright (C) 2013  Wilco Terink
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Email: w.terink@futurewater.nl OR terinkw@gmail.com

#-Authorship information-###################################################################
__author__ = "Wilco Terink"
__copyright__ = "Wilco Terink"
__license__ = "GPL"
__version__ = "erosion testing"
__email__ = "w.terink@futurewater.nl, terinkw@gmail.com"
__date__ ='1 January 2017'
############################################################################################

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

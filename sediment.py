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

#- Equations to calculate sediment yield accoding to the soil loss equation (Williams, 1995)

print 'Sediment module imported'

#-Modified unviversal soil loss equation to calculate sediment yield (metric tons)
def Musle(self, pcr, Q_surf, q_peak):
    sed = 11.8 * (Q_surf * q_peak * self.ha_area)**0.56 * self.K_USLE * self.C_USLE * \
        self.P_USLE * self.LS_USLE * self.CFRG
    sed = (sed / 10000) * pcr.cellarea()  # conversion to ton / cell area [m2]
    return sed
    
#-Peak runoff (m3/s)    
def q_peak(self, pcr, RootRunoff):
    q_peak = (self.Alpha_tc * RootRunoff * pcr.cellarea()) / (3600000 * self.Tc)  # peak runoff in m3/s
    return q_peak
    
#-LS topographic factor
def LS_ULSE(self, pcr):
    m = 0.6 * (1 - pcr.exp(-35.835 * self.Slope))
    alpha_hill = pcr.atan(self.Slope)
    L_hill = pcr.celllength() / pcr.cos(alpha_hill)
    LS = ((L_hill / 22.1)**m) * (65.41 * pcr.sin(alpha_hill)**2 + 4.56 * pcr.sin(alpha_hill) + 0.065)
    return LS

#-Time of concentration
def Tc(self, pcr):
    slope_adjusted = pcr.ifthenelse(self.Slope < 0.0025, self.Slope + 0.0005, self.Slope)
    alpha_hill = pcr.atan(slope_adjusted)
    L = pcr.celllength() / pcr.cos(alpha_hill)
    #-Kirpich channel flow time of concentration
    T_ch = 0.0195 * L**0.77 * slope_adjusted**-0.385
    #-Kerby overland flow time of concentration
    T_ov = 1.44 * (L * self.N)**0.467 * slope_adjusted**-0.235
    Tc = (T_ch + T_ov) / 60  # conversion to hours
    return Tc

#-Routing of sediment
def SRout(self, pcr, sed):
    sr = pcr.accuflux(self.FlowDir, sed)
    sr = (1 - self.kx) * sr + self.kx * self.SYieldR
    return sr
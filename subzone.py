# -*- coding: utf-8 -*-
#
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
# Email: terinkw@gmail.com

#-Authorship information-###################################################################
__author__ = "Wilco Terink"
__copyright__ = "Wilco Terink"
__license__ = "GPL"
__version__ = "2.2"
__email__ = "terinkw@gmail.com"
__date__ ='16 October 2018'
############################################################################################

#-Function to calculate capillary rise
def CapilRise(pcr, subfield, subwater, capmax, rootwater, rootsat, rootfield):
    subrelwat = pcr.max(pcr.min((subwater / subfield), 1), 0)
    rootrelwat = pcr.max(pcr.min((rootwater / rootfield), 1), 0)
    caprise = pcr.min(subwater, capmax * (1 - rootrelwat) * subrelwat)
    caprise = pcr.min(caprise, rootsat - rootwater)  # adding caprise can not exceed saturated rootwater content
    return caprise

#-Function to calculate percolation from subsoil (only if groundwater module is used)
def SubPercolation(pcr, subwater, subfield, subTT, gw, gwsat):
    subperc =  pcr.ifthenelse((gw < gwsat) & ((subwater - subfield) > 0), (subwater - subfield) * (1 - pcr.exp(-1 / subTT)), 0)
    return subperc

#-Function to calculate drainage from subsoil (only if groundwater module is NOT used)
def SubDrainage(pcr, subwater, subfield, subsat, drainvel, subdrainage, subTT):
    subexcess = pcr.max(subwater - subfield, 0)
    subexcessfrac = subexcess / (subsat - subfield)
    sublateral = subexcessfrac * drainvel
    subdrainage = (sublateral + subdrainage) * (1 - pcr.exp(-1 / subTT))
    subdrainage = pcr.max(pcr.min(subdrainage, subwater), 0)
    return subdrainage
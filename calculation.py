import numpy as np

class Calculation():
    
    def __init__(self, parameters):
        Rm, Rp, E, opt = parameters[0], parameters[1], parameters[2], parameters[3]
        
        # väsymisrajan oletusarvo (3.8)
        ### KORJAUS 17.2.2025: Vaihdettu 0.390 kerroin 0.309 ###
        s_aR1 = 1.04*(0.144*Rm+0.309*Rp)+56
        #s_aR1 = 0.47 * Rm


        
        
        # lineaarisen osan kaltevuuskerroin (3.10)
        k = 0.1-0.00035*Rm
        
        # väsymisraja tykyttävällä kuormalla (3.11)
        s_aR0 = s_aR1/(1-k)
        
        # keskijännitys tykyttävällä kuormalla (3.12)
        s_mR0 = s_aR0
        
        # apusuureet
        M = -k
        b = (2*(1+2*M)) / (2+2*M-M**2)
        
        # fiktiivinen murtoraja
        if opt:
            R_mf = 1.3 * Rm
        else:
            R_mf = ((1+2*M)*s_aR1) / (M*(2+M))
        
        # alkupiste
        s_mP0 = -R_mf
        s_aP0 = 0
        
        # kontrollipiste 1
        s_mP1 = (R_mf-s_aR1)/(k-1)
        s_aP1 = R_mf+s_mP1
        
        # kontrollipiste 2
        s_mP2 = (s_aR1-Rp)/(2*(1-k))
        s_aP2 = s_aR1+k*s_mP2
        s_m2 = s_mP2
        
        
        # keskijännitys
        s_m3 = np.linspace(-R_mf, s_m2)
        s_m = np.linspace(s_m2, s_mR0)
        s_m2 = np.linspace(s_mR0, R_mf)
        
        # haig diagrammin suora osuus (3.13a)
        s_af = s_aR1+k*s_m
        
        # vetopuolen paraabeli (3.17)
        s_af2 = s_aR1*((1-b)/(2-b) + np.sqrt(1/((2-b)**2) - (b*s_m2)/((2-b)*R_mf)))
        
        # negatiivisen puolen paraabeli
        if (s_mP0-s_mP1)/(s_mP0-2*s_mP1+s_mP2) > 0:
            t = (s_mP0-s_mP1)/(s_mP0-2*s_mP1+s_mP2) - np.sqrt(((s_mP0-s_mP1)/(s_mP0-2*s_mP1+s_mP2))**2 - (s_mP0-s_m3)/(s_mP0-2*s_mP1+s_mP2))
        else:
            t = (s_mP0-s_mP1)/(s_mP0-2*s_mP1+s_mP2) + np.sqrt(((s_mP0-s_mP1)/(s_mP0-2*s_mP1+s_mP2))**2 - (s_mP0-s_m3)/(s_mP0-2*s_mP1+s_mP2))
        
        s_af3 = (1-t)**2*s_aP0+2*t*(1-t)*s_aP1+t**2*s_aP2
        
        
        # muokkaa lineaarista osaa jos valittu opt
        if opt:
            s_af = np.linspace(s_af3[-1], s_af2[0], num=len(s_m))
            
        # aloituspiste morrowin ja goodmanin suorille jos modifioitu lineaariosa
        if opt:
            idx = np.rint(-s_mP2/((s_mR0-s_mP2)/ len(s_m2)))
            start_y = s_af[int(idx)]
        else:
            start_y = s_aR1
            
        
        
        # morrow mean stress correction
        self.s_m4 = np.linspace(0, R_mf)
        self.s_af4 = np.linspace(start_y, 0)
        
        # goodman mean stress correction
        self.s_m5 = np.linspace(0, Rm)
        self.s_af5 = np.linspace(start_y, 0)
        
        self.s_m = s_m
        self.s_m2 = s_m2
        self.s_m3 = s_m3
        self.s_af = s_af
        self.s_af2 = s_af2
        self.s_af3 = s_af3

    def get_curves(self):
        return [self.s_m, self.s_m2, self.s_m3, self.s_af, self.s_af2, self.s_af3, self.s_m4, self.s_m5, self.s_af4, self.s_af5]
    
        






























        
        

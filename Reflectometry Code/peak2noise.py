import numpy as np

def peak2noise(f, p, frange):
    # Find index of the maximum amplitude of LSP
    ij = np.argmax(p)
    
    # Max amplitude of LSP
    maxRHAmp = p[ij]
    
    # Reflector height corresponding to max value
    maxRH = f[ij]
    
    # Find indices within the frequency range
    i = np.where((f > frange[0]) & (f < frange[1]))[0]
    
    # Calculate noise value
    noisey = np.mean(p[i])
    
    # Divide into the max amplitude
    pknoise = maxRHAmp / noisey
    
    return maxRH, maxRHAmp, pknoise
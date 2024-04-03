import numpy as np

def lomb(t,h,ofac,hifac):
    # Sample length and time span
    N = len(h)
    T = max(t) - min(t)

#     # Print the values for debugging
#     print("N:", N)
#     print("T:", T)
#     print("ofac:", ofac)
#     print("hifac:", hifac)

    # Mean and variance
    mu = np.mean(h)
    s2 = np.var(h)

    # Calculate sampling frequencies
    if T > 0 and np.isfinite(ofac):
        f = np.arange(1 / (T * ofac), hifac * N / (2 * T), 1 / (T * ofac))
    else:
#         print(T)
#         print(ofac)
        print(t)
        print(h)
        
        print("Invalid values for T or ofac. Cannot compute sampling frequencies.")

    # Angular frequencies and constant offsets
    w = 2 * np.pi * f
    tau = np.arctan2(np.sum(np.sin(2 * w * t[:, np.newaxis]), axis=0),
                     np.sum(np.cos(2 * w * t[:, np.newaxis]), axis=0)) / (2 * w)
    
    
    # Spectral power
    cterm = np.cos(w * t[:, np.newaxis] - w * tau)
    sterm = np.sin(w * t[:, np.newaxis] - w * tau)

    P = (np.sum(cterm * (h[:, np.newaxis] - mu), axis=0)**2 / np.sum(cterm**2, axis=0) + np.sum(sterm * (h[:, np.newaxis] - mu), axis=0)**2 / np.sum(sterm**2, axis=0)) / (2 * s2)


    # Estimate of the number of independent frequencies
    M = 2 * len(f) / ofac

    # Statistical significance of power (alarm probability)
    prob = M * np.exp(-P)
    inds = prob > 0.01
    prob[inds] = 1 - (1 - np.exp(-P[inds]))**M

    # Amplitude
    P = 2 * np.sqrt(s2 * P / N)

    # 95% confident level amplitude
    cf = 0.95
    cf = 1 - cf
    conf95 = -np.log(1 - (1 - cf)**(1 / M))
    conf95 = 2 * np.sqrt(s2 * conf95 / N)

    return f, P, prob, conf95
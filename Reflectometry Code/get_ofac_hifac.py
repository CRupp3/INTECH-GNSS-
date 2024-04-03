import numpy as np

def get_ofac_hifac(elevAngles, cf, maxH, desiredPrecision):
    # SNR expressed as a function of X
    X = np.sin(np.deg2rad(elevAngles)) / cf  # in units of inverse meters

    # Number of observations
    N = len(X)

    # Observing window length (or span)
    W = np.max(X) - np.min(X)  # units of inverse meters

    # Characteristic peak width
    characteristic_peak_width = 1 / W  # in meters

    # Oversampling factor
    ofac = characteristic_peak_width / desiredPrecision

    # Nyquist frequency if the N observed data samples were evenly spaced
    # over the observing window span W
    fc = N / (2 * W)  # in meters

    # The high-frequency factor is defined relative to fc
    hifac = maxH / fc

    return ofac, hifac
    
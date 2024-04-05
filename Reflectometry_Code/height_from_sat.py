import numpy as np
import matplotlib.pyplot as plt
from read_QC import read_QC
from quality_control_filter import quality_control_filter
from get_wavelength import get_wavelength
from get_ofac_hifac import get_ofac_hifac
from peak2noise import peak2noise
from lomb import lomb

def height_from_sat(group, QC_filename, dynamic, year, doy, interpolate, printFailReasons, showAllPlots):
    # Obtain the QC parameters
    [emin, emax, ediff, maxHeight, desiredPrecision, frange_0, frange_1, minAmp, minRH, maxArcTime, pknoiseCrit, azmin, azmax] = read_QC(QC_filename)
    #Filter based off of QC parameters
    filtered_group = quality_control_filter(group, QC_filename)
    
    # Check for missing values in 'satID' after filtering
    if filtered_group['satID'].isnull().any():
        print("Warning: Found missing values in 'satID' after filtering. Rows will be skipped.")
        return None  # Skip processing for this group
    
    SNR_data = filtered_group['SNR_data']

    # Obtain the wavelength factor for this specific satellite 
    WL, freqtype = get_wavelength(filtered_group)
    if WL is not None:
        WLF = WL/2 
    else:
        #print("Error: Wavelength factor is not available.")
        return None 

    if interpolate: #If we want to interpolate (necessary if elevation precision is low)
        elevAngles = filtered_group["elevAng"].values # Elevation angles in degrees
        time = filtered_group["gpsTime"].values / 3600  # UTC hours
        data = 10**(filtered_group["SNR_data"].values / 20)  # Change SNR data from dB-Hz to linear units
        azm = np.mean(filtered_group["azAng"].values)  # Average azimuth for a track, in degrees
        raw_data = data
        raw_elevAngles = elevAngles
        
        poly_time_sEle = np.polyfit(time, np.sin(np.radians(elevAngles)), 1)
        interp_sinE = np.polyval(poly_time_sEle, time)
        elevAngles = np.rad2deg(np.arcsin(interp_sinE))
    
    else: #If we do not need to interpolate (when elevation data has high precision)
        elevAngles = filtered_group["elevAng"].values # Elevation angles in degrees
        time = filtered_group["gpsTime"].values / 3600  # UTC hours
        data = 10**(filtered_group["SNR_data"].values / 20)  # Change SNR data from dB-Hz to linear units
        azm = np.mean(filtered_group["azAng"].values)  # Average azimuth for a track, in degrees
        raw_data = data
        raw_elevAngles = elevAngles
    

    if filtered_group['elevAng'].nunique() == 1: #Make sure there is enough informaton to be useful
        return None  # Return an empty DataFrame (NaN)

    # Time span of the track in hours
    dt = time[-1] - time[0]

    # Remove direct signal
    p = np.polyfit(elevAngles, data, 1)
    pv = np.polyval(p, elevAngles)

    # Sine of elevation angles
    sineE = np.sin(np.deg2rad(elevAngles))

    # Remove the direct signal with a polynomial
    saveSNR = data - pv

    # Get the oversampling factor and hifac
    ofac, hifac = get_ofac_hifac(elevAngles, WLF, maxHeight, desiredPrecision)

    # Call the Lomb-Scargle code
    f, p, _, _ = lomb(sineE/WLF, saveSNR, ofac, hifac)
    maxRH, maxRHAmp, pknoise = peak2noise(f, p, [frange_0, frange_1])

    # Max reflector height should be more than 2*lambda, or ~40-50 cm
    # Restrict arcs to be < one hour. Long dt usually means you have a track that goes over midnight
    maxObsE = np.max(elevAngles)
    minObsE = np.min(elevAngles)
        
    if showAllPlots:   
        if len(elevAngles) < 2:
            print("Warning: Insufficient data for plotting.")
        else:
            # Create subplots
            fig, axes = plt.subplots(2, 2, figsize=(12, 12))

            # Plot SNR_data vs sin(elevAng)
            axes[0, 0].plot(np.sin(np.radians(raw_elevAngles)), raw_data, label='Raw_SNR_data vs sin(elevAng)')
            axes[0, 0].set_xlabel('sin(elevAng)')
            axes[0, 0].set_ylabel('Raw_SNR_data')
            axes[0, 0].set_title('Raw_SNR_data vs sin(elevAng)')
            axes[0, 0].legend()

            # Plot sin(elevAng) vs time
            axes[0, 1].plot(time, np.sin(np.radians(elevAngles)), label='Corrected Elevation Angles')
            if interpolate: 
                axes[0, 1].plot(time, np.sin(np.radians(raw_elevAngles)),label='Raw Elevation Angles' )
            axes[0, 1].set_xlabel('Time')
            axes[0, 1].set_ylabel('sin(elevAng)')
            axes[0, 1].set_title('sin(elevAng) vs Time')
            axes[0, 1].legend()

            # Plot saveSNR vs sin(elevAng)
            axes[1, 0].plot(np.sin(np.radians(elevAngles)), saveSNR, label='De-trended SNR vs sin(elevAng)')
            axes[1, 0].set_xlabel('sin(elevAng)')
            axes[1, 0].set_ylabel('De-trended SNR')
            axes[1, 0].set_title('De-Trended SNR vs sin(elevAng)')
            axes[1, 0].legend()

            # Plot periodogram
            axes[1, 1].plot(f, p, label='Periodogram')
            axes[1, 1].set_xlabel('Reflector Height [m]')
            axes[1, 1].set_ylabel('Power')
            axes[1, 1].set_title('Periodogram')
            axes[1, 1].legend()


            # Adjust layout to prevent overlap
            plt.tight_layout()

            # Show the subplots
            plt.show()

            
    #If we are within quality control bounds 
    if maxRHAmp > minAmp and maxRH > minRH and dt < maxArcTime and pknoise > pknoiseCrit and (maxObsE - minObsE) > ediff:
        if showAllPlots: 
            print(f'RH: {maxRH:.2f}, RHAmp: {maxRHAmp:.2f}, Azm: {azm:.1f}, Constellation: {filtered_group["constellation"].values[0]}, SatID: {filtered_group["satID"].values[0]:.0f}, Tdiff: {dt * 60:.0f}, ' f'Emin: {minObsE:.2f}, Emax: {maxObsE:.2f}, Peak2Noise: {pknoise:.2f}, FreqType: {freqtype}, MeanTime: {np.mean(time):.2f}')
        if dynamic: 
            # Calculate the average time
            avg_time = np.mean(time)

            # Find the nearest time points surrounding the average time
            nearest_indices = np.argsort(np.abs(time - avg_time))[:2]

            # Interpolate elevAngles at the nearest time points
            elevAngles_at_avg_time = np.interp(avg_time, time[nearest_indices], elevAngles[nearest_indices])

            # Estimate the slope using numerical differentiation
            delta_time = np.diff(time[nearest_indices])[0]
            delta_elevAngles = np.diff(elevAngles[nearest_indices])[0]
            edot_at_avg_time = delta_elevAngles / delta_time
            
            tan_elevAngle_at_avg_time = np.tan(elevAngles_at_avg_time)


            
            #Retrun values needed for dynamic height correction 
            return maxRH, tan_elevAngle_at_avg_time, edot_at_avg_time
        
        else: 
            return maxRH, None, None
    #If we are not within QC bounds print reason for failure 
    else:
        fail_reasons = []
        if maxRHAmp <= minAmp:
            fail_reasons.append("Amp")
        if maxRH <= minRH:
            fail_reasons.append("RH")
        if dt >= maxArcTime:
            fail_reasons.append("Tdiff")
        if pknoise <= pknoiseCrit:
            fail_reasons.append("Peak2Noise")
        if (maxObsE - minObsE) <= ediff:
            fail_reasons.append("Emin/Emax difference")
        if printFailReasons:
            print(f'Fail QC ({", ".join(fail_reasons)}) RH {maxRH:.2f} Amp {maxRHAmp:.2f} Azm {azm:.1f} Sat {filtered_group["constellation"].values[0]} {filtered_group["satID"].values[0]:.0f} ' f'Tdiff {dt * 60:.0f} Emin {minObsE:.2f} Emax {maxObsE:.2f} Peak2Noise {pknoise:.2f}')
        return None
    return None
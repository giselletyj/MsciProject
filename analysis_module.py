import matplotlib.pyplot as plt
import numpy as np
import ruptures as rpt
from scipy import signal

def rupture_force_analysis(time_array, signal_array, force_array, start_time, step=100):
    start_point = int(start_time*0.05**-1)
    interval = int(45*0.05**-1)
    end = start_point + int(40*0.05**-1)
    extension_location = []
    
    while end < len(signal_array):
        plt.figure(figsize=(15,3))
        plt.plot(time_array[start_point:end], signal_array[start_point:end])
        plt.xlabel('Time')
        plt.ylabel('Signal')
        plt.title(f"Slice {start_point} to {end}")
        plt.show()
        
        user_input = input("Is this the correct slice? (y/n/stop): ").lower()
        
        if user_input == 'y':
            
            algo = rpt.Pelt(model="l2", min_size=50)
            algo.fit(np.array(signal_array[start_point:end]))
            result = algo.predict(pen=1)
            
            new_result = np.zeros(len(result)-1)
            for i in range(len(result)-1):
                new_result[i] = time_array[start_point:end][result[i]]
                
            plt.figure(figsize=(15,3))
            plt.plot(time_array[start_point:end], signal_array[start_point:end])
            plt.title(f"Slice {start_point} to {end}")
            plt.xlabel('Time (seconds)')
            plt.ylabel('Extension signal')
            plt.vlines(new_result, 
                       ymin=min(signal_array[start_point:end]), 
                       ymax=max(signal_array[start_point:end]),
                       colors='black', linestyle='--',linewidth=2, label='Change Points')
            plt.legend()
            plt.show()
            
            start_point = end
            end = start_point + interval
            
            #Make sure there are at least 3 change lines in graph
            #Each change line counts by 0,1,2
            user_input_2 = input("Insert change point number (0/1/2/3/4/5/none): ").lower()
            
            if user_input_2 == '0':
                extension_location.append(new_result[0])
            
            elif user_input_2 == '1':
                extension_location.append(new_result[1])
            
            elif user_input_2 == '2':
                extension_location.append(new_result[2])
                
            elif user_input_2 == '3':
                extension_location.append(new_result[3])
                
            elif user_input_2 == '4':
                extension_location.append(new_result[4])
                
            elif user_input_2 == '5':
                extension_location.append(new_result[5])
                
            elif user_input_2 == '6':
                extension_location.append(new_result[6])
            
            elif user_input_2 == '7':
                extension_location.append(new_result[7])
                
            elif user_input_2 == '8':
                extension_location.append(new_result[8])
        
            elif user_input_2 == '9':
                extension_location.append(new_result[9])
                
            elif user_input_2 == 'none':
                extension_location.append(np.nan)

            
        elif user_input == 'n':
            direction = input("Move plot axis to right or left? (r/l): ").lower()
            if direction == 'r':
                start_point += step
                end += step
            elif direction == 'l':
                start_point -= step
                end -= step
                if start_point < 0:
                    print("Cannot move further left. Resetting.")
                    star_point = start_time*0.05**-1
                    end = start_point + step
            else:
                print("Invalid input. Please enter 'r' or 'l'.")
        
        elif user_input == 'stop':
            print("Done processing")
            print(extension_location)
            break
            
        plt.close()
    
    force_location = np.zeros(len(extension_location))
    extension_location_2 = np.zeros(len(extension_location),dtype=int)
    for i in range(len(extension_location)):
        if not np.isnan(extension_location[i]) and extension_location[i] != -1:
            extension_location_2[i] = int(extension_location[i]*0.05**-1)
            force_location[i] = force_array[extension_location_2[i]]
        else:
            extension_location_2[i] = 0  # Convert the special value back to NaN
            force_location[i] = 0
            


    print("Finished processing.")
    print(force_location)
    
    
    return force_location, extension_location


def rupture_times_analysis(time_array, signal_array, start_time, interval_step, step=20):
    
    start_point = start_time*0.05**-1
    interval = interval_step*0.05**-1
    end = start_point + 64.5*0.05**-1
    time_result = []
    
    b, a = signal.butter(3, 0.05, btype='lowpass', analog=False)
    low_passed = signal.filtfilt(b, a, signal_array)
    
    while end < len(low_passed):
        plt.figure(figsize=(15,3))
        plt.plot(time_array[int(start_point):int(end)], low_passed[int(start_point):int(end)])
        plt.xlabel('Time')
        plt.ylabel('Signal')
        plt.title(f"Slice {start_point} to {end}")
        plt.show()
        
        user_input = input("Is this the correct slice? (y/n/stop): ").lower()
        
        if user_input == 'y':
            
            algo = rpt.Pelt(model="l1", min_size=5)
            algo.fit(np.array(low_passed[int(start_point):int(end)]))
            result = algo.predict(pen=1)
            
            new_result = np.zeros(len(result)-1)
            for i in range(len(result)-1):
                new_result[i] = time_array[int(start_point):int(end)][result[i]]
                
            plt.figure(figsize=(15,3))
            plt.plot(time_array[int(start_point):int(end)], low_passed[int(start_point):int(end)])
            plt.title(f"Slice {start_point} to {end}")
            plt.xlabel('Time (seconds)')
            plt.ylabel('Extension signal')
            plt.vlines(new_result, 
                       ymin=min(low_passed[int(start_point):int(end)]), 
                       ymax=max(low_passed[int(start_point):int(end)]),
                       colors='black', linestyle='--',linewidth=2, label='Change Points')
            plt.legend()
            plt.show()
            
            start_point = end
            end = start_point + interval
            
            #Make sure there are at least 3 change lines in graph
            #Each change line counts by 0,1,2
            user_input_2 = input("Insert change point number (2/3/4/5): ").lower()
            
            if user_input_2 == '0':
                time_result.append(0)
            
            if user_input_2 == '2':
                time_result.append(new_result[2]-new_result[1])
                
            elif user_input_2 == '3':
                time_result.append(new_result[3]-new_result[1])
                
            elif user_input_2 == '4':
                time_result.append(new_result[4]-new_result[1])
                
            elif user_input_2 == '5':
                time_result.append(new_result[5]-new_result[1])

            
        elif user_input == 'n':
            direction = input("Move plot axis to right or left? (r/l): ").lower()
            if direction == 'r':
                start_point += step
                end += step
            elif direction == 'l':
                start_point -= step
                end -= step
                if start_point < 0:
                    print("Cannot move further left. Resetting.")
                    star_point = start_time*0.05**-1
                    end = start_point + step
            else:
                print("Invalid input. Please enter 'r' or 'l'.")
        
        elif user_input == 'stop':
            print("Done processing")
            print(time_result)
            break
            

        plt.close()

    print("Finished processing.")
    return time_result
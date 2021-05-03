# delay calculator
import pandas as pd

# database creation to store variables(max,min,average), source_to_satellite_distance, source_latency, destination_to_satellite_distance,destination_delay
column_name  = ['variable','source_sat_dist','source_latency','dest_sat_dist','dest_latency']
database = pd.DataFrame(columns = column_name)


channel_load_multiplier= None


# function to generate channel_load_multiplier value based on the channel load
def channel_load_func(input_val):

    while True:
        if input_val<0.5:
            channel_load_multiplier = 1.2
            break
        elif (input_val>=0.5 and input_val<0.6):
            channel_load_multiplier = 1.75
            break
        elif (input_val>=0.6 and input_val<0.75):
            channel_load_multiplier = 1.8
            break
        else:
            print(" Please enter value between 0.0 and 0.75")
    return(channel_load_multiplier)


# function to take user input regarding the window size
def window_size_func():
    #units in Bits
    while True:             # Loop continuously
        inp = int(input(" Enter window size in Bytes: "))
        if inp <1073741824:
            window_size = inp* (9.537*10**(-7)) *8 # conversion from bytes to Mega bits 
            break
        else:
            print(" Error: Standard TCP/IP allows a maximum window size of 1073741824 bytes")
            # change it to 1 GB

# database to store predefined latency values
def database_creation():

    database.loc[0,'variable'] = 'max'
    database.loc[1,'variable'] = 'min'
    database.loc[2,'variable'] = 'avg'
    
    database.loc[database['variable'] == 'max','source_latency'] = 37.3
    database.loc[database['variable'] == 'min','source_latency'] = 31.4
    database.loc[database['variable'] == 'avg','source_latency'] = 32.9    

    database.loc[database['variable'] == 'max','dest_latency'] = 191.6
    database.loc[database['variable'] == 'min','dest_latency'] = 31.4
    database.loc[database['variable'] == 'avg','dest_latency'] = 106.5    
    
# function to take user input regarding the source to satellite and satellite to source distance
def dist_func():
    max_source_satellite_dist = float(input(" Enter maximum source to satellite distance in Kilometers: "))
    min_source_satellite_dist = float(input(" Enter minimum source to satellite distance in Kilometers: "))
    avg_source_satellite_dist = float(input(" Enter average source to satellite distance in Kilometers: "))
    
    database.loc[database['variable'] == 'max','source_sat_dist'] = max_source_satellite_dist
    database.loc[database['variable'] == 'min','source_sat_dist'] = min_source_satellite_dist
    database.loc[database['variable'] == 'avg','source_sat_dist'] = avg_source_satellite_dist
                
    max_dest_satellite_dist = float(input(" Enter maximum satellite to destination distance in Kilometers: "))
    min_dest_satellite_dist = float(input(" Enter minimum satellite to destination distance in Kilometers: "))
    avg_dest_satellite_dist = float(input(" Enter average satellite to destination distance in Kilometers: "))

    database.loc[database['variable'] == 'max','dest_sat_dist'] = max_dest_satellite_dist
    database.loc[database['variable'] == 'min','dest_sat_dist'] = min_dest_satellite_dist
    database.loc[database['variable'] == 'avg','dest_sat_dist'] = avg_dest_satellite_dist

# function to calculate transmission delay
def transmission_delay_func(packet_size, channel_load_multiplier):
    tcp_delay = float(input(" Enter TCP delay in %: "))
    uplink_data_rate = float(input(" Enter the Uplink Rate : "))/channel_load_multiplier
    downlink_data_rate = float(input("Enter the Downlink Rate : "))
    data_rate = min(uplink_data_rate, downlink_data_rate) 
    data_rate = data_rate*((100-tcp_delay)/100)
    transmission_delay = (packet_size*8)/(data_rate) #Changing the byte to bit
    return transmission_delay

# function to calculate up_link_delay
def up_link_delay_func(speed_of_signal,channel_load_multiplier):
    return (database['source_sat_dist']/speed_of_signal)*channel_load_multiplier

# function to calculate down_link_delay
def down_link_delay_funct(speed_of_signal):
    return  database['source_sat_dist']/speed_of_signal

#function to calculate inter satellite delay
def inter_sat_link_delay_funct():
    inter_sat_link_delay = 0.0

#function to calculate switching delay
def switching_delay_func():
    switching_delay = 0.0

#function to calculate buffering delay
def buffering_delay():
    buffering_delay = 0.0
    
#function to calculate end to end delay
def end_to_end_delay(packet_size,source_satellite_dist,speed_of_signal,dest_satellite_dist,channel_load_multiplier):
    delay = transmission_delay_func(packet_size, channel_load_multiplier)+ up_link_delay_func(speed_of_signal,channel_load_multiplier)+down_link_delay_funct(speed_of_signal)+2*(10**(-3))
    return list(delay)

#function to calculate security
def security_delay():
    pass

   


def main():

        database_creation()
        packet_size = float(input(" Enter Packet Size in MB: "))
        channel_load_multiplier = channel_load_func(float(input(" Enter the Value of Channel Load (Min: 0.0 Max: 0.75): " )))
        window_size = window_size_func()
        trans_delay = transmission_delay_func()
        dist_func()  
        speed_of_signal = float(input(" Enter Speed of Signal in Thousand Kilometers per Second: "))*(10**5)
        delay_result = end_to_end_delay(packet_size,database['source_sat_dist'],speed_of_signal,database['source_sat_dist'],channel_load_multiplier)
        df = pd.DataFrame(delay_result,index = ['Max','Min','Avg'],columns = ['Value in seconds'])
        print("*** Calculating Delay ***")
        print("delay",df)       

if __name__=="__main__":
    main()


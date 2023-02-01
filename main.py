import numpy as np
import random


class parking_lot:
    def __init__(self, plot_size = 2000 , ps_size= 96):
        self.plot_size, self.ps_size = plot_size, ps_size           # setting parking lot and parking spot sizes
        self.possible_size = self.plot_size // self.ps_size         # calculating possible no of slots based on parking lot and parking spot sizes
        self.aval_slots = np.empty(self.possible_size, dtype=object)
        self.is_full = False
        self.consumed_slots = 0
    
    def allot_parking_spot(self, car_object, req_spot):
        if self.consumed_slots == self.possible_size:
            self.is_full = True
        req_spot = req_spot - 1                                     # indexing adjustments
        if req_spot > self.aval_slots.size:                         # out of bound check
            return [False, f'There are only {self.possible_size} Parking Slots in This Parking Lot']
        elif self.aval_slots[req_spot] != None:                     # checking if required slot is available
            return [False, f'Parking Spot is taken by car with license plate {self.aval_slots[req_spot].license_plate}']
        else:
            self.consumed_slots += 1
            self.aval_slots[req_spot] = car_object                  # slot allotment
            return [True]
    
    def display_current_state(self, generatejson=True):             # to display state of entire parking lot and generate JSON Object
        taken_ctr = 0
        print('\n\n\t\t Current Parking Lot Status\n\n')
        if generatejson:
            string = '' 
            json_string = '{ '
        for i in range(0, self.possible_size):
            if self.aval_slots[i] != None:
                taken_ctr += 1
                if generatejson:
                    string += f'"slot{i+1}" : "{self.aval_slots[i].license_plate}", '
                print(f'\tcar with license plate {self.aval_slots[i].license_plate} is parked at spot no {i+1}')
            else:
                if generatejson:
                    string += f'"slot{i+1}" : "EMPTY", '
        
        if generatejson:
            json_string += '"parking_lot":{'+f'{string[:-2]}'+'}'
            json_string += ' }'
        
        # saving JSON object
        print(f'\nNo Of Available Slots : {self.possible_size-taken_ctr}')
        if generatejson:
            import os
            with open('parking_lot.json', 'w') as f:
                f.write(json_string)
            print(f'\n\nJSON File with name parking_lot.json was saved at {os.getcwd()}\\ \n\n')


class car:
    def __init__(self, license_plate):
        if len(license_plate) > 7:
            print('\tWarning: License Plate Can Only Be 7 Digits')
        self.license_plate = license_plate[:7]                      # setting license plate parameter
        self.parking_spot = None                                    # optional (can be used for indexing using number plate in future)
    
    def __str__(self):                                              # overriding default magic method to print licence plate while string conversion
        print(f'License Plate : {self.license_plate}')
        return f'License_Plate: {self.license_plate}, Parking_Spot: {self.parking_spot}'
    
    def park(self, parking_lot,spot_no):
        ret = parking_lot.allot_parking_spot(self, spot_no)         
        if ret[0] == True:
            print(f'Car With License Plate {self.license_plate} Parked Successfully at Spot No : {spot_no}\n')
            self.parking_spot = spot_no
            return True
        else:
            print(f'\nCould Not Park the Car {self.license_plate} at Spot {spot_no}\n\tReason {ret[1]}\n')
            return False
        
    


def main(licence_plate_list):
    pl = parking_lot()
    random_limit = 20                                               # to set limit on random number generation

    for lp in licence_plate_list:
        c1 = car(license_plate=lp)
        state = False
        while state != True:
            state = c1.park(pl, spot_no=random.randint(0,random_limit))# try to park at random spot and get state
            if pl.is_full:
                print('Parking Lot Full\nTerminating Program....')
                break
    pl.display_current_state()


if __name__ == '__main__':
    l_list = ['ABC1323', 'DEF4564', 'HIJ7486', 'KLM7392', 'NOP0938', 'QRS9843', 'TUV03473', 'WXYZ830']
    main(l_list)



# Explainations

# class parking_lot
    # allot_parking_spot
        # This function tries to allot requested parking spot
            # if the spot is available true is returned otherwise reason for no allotment is returned
        
    # display_current_state
        # This function displays current state of entire parking lot and generates JSON object and saves in a file


# class car
    # park
        # This function tries to get a parking lot and prints if it was successful or not

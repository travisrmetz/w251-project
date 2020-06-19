import yaml
import subprocess
import geopy
from sky_helper import next_lat, next_long,get_file_name

def main():
    """
    Parses a YAML file containing lists of positions from which to
    collect images.  Generates a ssc script to automate the process
    in Stellarium.  Runs the ssc script in Stellarium.
    
    TODO: Save resulting images to a cloud object store.
    """
    # Parse the yaml file
    with open('ssc_generator.yml') as config_file:
        # The default version of Pyyaml with the NVIDIA image does
        # not include FullLoader, so we have to fall back to the
        # pre-2019 syntax
        config_data = yaml.load(config_file)
    
    #TODO:  This can be done better with an eval function and a loop
    script_path = config_data['script_path']
    image_dir = config_data['image_path']
    azi = config_data['azi']
    alt = config_data['alt']
    fov = config_data['fov']
    latstart = config_data['latstart']
    latend=config_data['latend']
    meters_lat_slice=config_data['meters_lat_slice']
    longstart = config_data['longstart']
    longend=config_data['longend']
    meters_long_slice=config_data['meters_long_slice']
    date = config_data['date']

    # Write the ssc file
    image_index = 0
    with open(script_path + 'get_multi_sky.ssc', 'w') as f:
        # TODO:  Add statements to eliminate labels in the images.
        # TODO:  Allow time to be read in as a list (move the following
        #        line to the loop).
        #f.write('core.setDate("{}", "utc");\n'.format(date))
        #f.write('LandscapeMgr.setFlagAtmosphere(true);\n')
        #f.write('StelMovementMgr.zoomTo({},0);\n'.format(fov))
        #f.write('core.setGuiVisible(false);\n')
        i=latstart
        j=longstart
        #print ('latstart,latend:',latstart,latend)
        #print('longstart,longend',longstart,longend)
        image_counter=0
        while j<longend:
            while i<latend:
                f.write('core.setDate("{}", "utc");\n'.format(date))
                f.write('LandscapeMgr.setFlagAtmosphere(true);\n')
                f.write('StelMovementMgr.zoomTo({},0);\n'.format(fov))
                f.write('core.setGuiVisible(false);\n')
                #print (i,j)
                #this does not seem to be working to eliminate labels
                #or somehow it just eliminates labels from first pic?
                f.write('StarMgr.setLabelsAmount(0);\n')
                f.write('SolarSystem.setFlagLabels(false);\n')
                f.write('MeteorShowers.setEnableMarker(false);\n')
                f.write('core.setObserverLocation({}, {}, 15, 1, "Ocean", "Earth");\n'.format(i, j))
                # The next statement needs to be repeated to generate stable images.
                # It seems that Stellarium doesn't like altitudes of 90 degrees.
                f.write('core.moveToAltAzi({}, {});\n'.format(alt, azi))
                file_name=get_file_name(i,j,date)
                f.write('core.screenshot("{}", invert=false, dir="{}", overwrite=true);\n'.format(get_file_name(i,j,date), image_dir))
                i=next_lat(i,j,meters_lat_slice)
                image_counter+=1
            i=latstart
            j=next_long(i,j,meters_long_slice)
        
        print('Creating #:', image_counter)
    
    # Open Stellarium and run the script
    proc_stellarium = subprocess.Popen(['stellarium', '--startup-script', 'get_multi_sky.ssc', '--screenshot-dir', image_dir], stdout=subprocess.PIPE)

if __name__ == "__main__":
    main()


#TODO
#get rid of labels
#set lens
#containerize
#confirm moving to S3
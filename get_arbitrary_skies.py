import yaml
import subprocess
import os
from ibm_botocore.client import Config
import ibm_boto3

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
    lat = config_data['lat']
    long = config_data['long']
    date = config_data['date']

    # Write the ssc file
    image_index = 0
    with open(script_path + 'get_multi_sky.ssc', 'w') as f:
        # TODO:  Add statements to eliminate labels in the images.
        # TODO:  Allow time to be read in as a list (move the following
        #        line to the loop).
        f.write('core.setDate("{}", "utc");\n'.format(date))
        f.write('LandscapeMgr.setFlagAtmosphere(true);\n')
        f.write('StelMovementMgr.zoomTo({},0);\n'.format(fov))
        f.write('core.setGuiVisible(false);\n')
        for i, j in zip(long, lat):
            f.write('core.setObserverLocation({}, {}, 15, 1, "Ocean", "Earth");\n'.format(i, j))
            # The next statement needs to be repeated to generate stable images.
            # It seems that Stellarium doesn't like altitudes of 90 degrees.
            f.write('core.moveToAltAzi({}, {});\n'.format(alt, azi))
            f.write('core.screenshot("{}", invert=false, dir="{}", overwrite=true);\n'.format('image' + str(image_index), image_dir))
            image_index += 1
        f.write('core.setGuiVisible(false);\n')
        f.write('core.quitStellarium();')
    
    # Open Stellarium and run the script
    proc_stellarium = subprocess.Popen(['stellarium', '--startup-script', 'get_multi_sky.ssc', '--screenshot-dir', image_dir], stdout=subprocess.PIPE)

    # write files to S3
    
    


if __name__ == "__main__":
    main()

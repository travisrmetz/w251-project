import yaml
import subprocess

def main():
    # Parse the yaml file
    with open('ssc_generator.yml') as config_file:
        config_data = yaml.load(config_file)
    
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
        f.write('core.setDate("{}", "utc");\n'.format(date)) # Eventually move into the loop
        f.write('LandscapeMgr.setFlagAtmosphere(true);\n')
        f.write('StelMovementMgr.zoomTo({},0);\n'.format(fov))
        f.write('core.setGuiVisible(false);\n')
        for i, j in zip(long, lat):
            f.write('core.setObserverLocation({}, {}, 15, 1, "Ocean", "Earth");\n'.format(i, j))
            f.write('core.moveToAltAzi({}, {});\n'.format(alt, azi)) # This has to be repeated to generate stable images, it seems
            f.write('core.screenshot("{}", invert=false, dir="{}", overwrite=true);\n'.format('image' + str(image_index), image_dir))
            image_index += 1
        f.write('core.setGuiVisible(true);')
        
    proc_stellarium = subprocess.Popen(['stellarium', '--startup-script', 'get_multi_sky.ssc', '--screenshot-dir', image_dir], stdout=subprocess.PIPE)

if __name__ == "__main__":
    main()

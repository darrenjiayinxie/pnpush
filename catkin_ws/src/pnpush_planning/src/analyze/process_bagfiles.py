#!/usr/bin/env python

# Peter KT Yu, Aug 2015
# main function to parse a folder of bagfiles 

import subprocess
import sys, os
import glob
import optparse

def main(argv):
    parser = optparse.OptionParser()
    parser.add_option('', '--noplotmotion', action="store_false", dest='plotmotion', 
                      help='Not do the plotting. ', default=True)
    parser.add_option('', '--plotmotion', action="store_true", dest='plotmotion', 
                      help='Do the plotting. ', default=True)
    parser.add_option('', '--noplotfmap', action="store_false", dest='plotfmap', 
                      help='Not do the friction map plotting. ', default=False)
    parser.add_option('', '--plotfmap', action="store_true", dest='plotfmap', 
                      help='Do the friction map plotting. ', default=False)
  
    (opt, args) = parser.parse_args()
                   
        
    dirname = args[0]
    filelist = glob.glob("%s/*.bag" % dirname)
    
    plotmotion = opt.plotmotion
    plotfmap = opt.plotfmap
    
    for bag_filepath in filelist:
        if not os.path.exists(bag_filepath.replace('bag','h5')):
            proc = subprocess.Popen('rosrun pnpush_planning parse_bagfile_to_rawjson.py %s --nojson' % (bag_filepath) , shell=True)
            proc.wait()
            
        if plotmotion and not os.path.exists(bag_filepath.replace('bag','png')):
            proc = subprocess.Popen('rosrun pnpush_planning plot_raw_json.py %s snapshots' % (bag_filepath.replace('.bag', '.json')) , shell=True)
            proc.wait()

        if plotfmap and not os.path.exists(bag_filepath.replace('.bag','_fmap.png')):
            proc = subprocess.Popen('rosrun pnpush_planning plot_friction_map.py %s' % (bag_filepath.replace('.bag', '.h5')) , shell=True)
            proc.wait()

if __name__=='__main__':
    main(sys.argv)
    

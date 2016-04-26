#!/usr/bin/env python

import sys, os, shutil, re, subprocess
from optparse import OptionParser


def make_filenamelist(input_dir):

    proc = subprocess.Popen( [ '/afs/cern.ch/project/eos/installation/cms/bin/eos.select', 'ls', input_dir ], stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
    output = proc.communicate()[0]
    if proc.returncode != 0:
        print output
        sys.exit(1)

    return output.splitlines()


def process_input_dir(input_dir, match, filelist):

    input_dir = input_dir.rstrip('/')+'/'
    filenamelist = make_filenamelist(input_dir)

    for filename in filenamelist:
        if( not re.search('.root$', filename) ):
            continue
        if ( match!=None and not re.search(match, filename) ):
            continue
        filelist.append(os.path.join(input_dir,filename))

    if( len(filelist)==0 ):
        print 'No matching .root files found'
        sys.exit()

    return


bash_template = """#!/bin/bash

START_TIME=`/bin/date`
echo "Started at $START_TIME"
echo ""

BATCHDIR=${PWD}

export SCRAM_ARCH=slc6_amd64_gcc491
cd MAIN_WORKDIR
eval `scram runtime -sh`

cp -v MAIN_WORKDIR/analysis.py $BATCHDIR/analysis.py

cd $BATCHDIR
echo "Running analysis job..."
python analysis.py --maxevents=-1 --print_every=1000 --input_file=INPUT_FILE
exitcode=$?

cp -v histo_mjj.root MAIN_WORKDIR/output/OUTPUT_FILENAME

echo ""
END_TIME=`/bin/date`
echo "Finished at $END_TIME"
exit $exitcode

"""


# usage description
usage = """Usage: python createAndSubmitJobs.py [options]\n
Example: python createAndSubmitJobs.py -w LXBatch_Jobs -i /eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_reduced/ScoutingPFHT__18_01_2016_20160118_170719/ -p /afs/cern.ch/user/l/lbajan/AnalysisTools/StandardAnalysis.py -m reduced_skim\n
For more help: python createAndSubmitJobs.py --help
"""

def main():
  # input parameters
  parser = OptionParser(usage=usage)

  parser.add_option("-w", "--main_workdir", dest="main_workdir", action='store', help="Main working directory", metavar="MAIN_WORKDIR")
  parser.add_option("-i", "--input_dir", dest="input_dir", action='store', help="Location of input files", metavar="INPUT_DIR")
  parser.add_option('-m', '--match', dest="match", action='store', help='Only files containing the MATCH string in their names will be considered (This parameter is optional)', metavar='MATCH')
  parser.add_option("-p", "--py_file", dest="py_file", action='store', help="Analysis python script", metavar="PY_FILE")
  parser.add_option('-f', '--fraction', dest='fraction', action='store', default='1.0', help='Fraction of files to be processed. Default value is 1 (This parameter is optional)', metavar='FRACTION')
  parser.add_option("-q", "--queue", dest="queue", action='store', default='1nh', help="LXBatch queue (choose among cmst3 8nm 1nh 8nh 1nd 1nw). Default is '8nh' (This parameter is optional)", metavar="QUEUE")
  parser.add_option("-n", "--no_submission", dest="no_submission", action='store_true', default=False, help="Create the necessary configuration files and skip the job submission (This parameter is optional)")
  

  (options, args) = parser.parse_args()

  # make sure all necessary input parameters are provided
  if not (options.main_workdir and options.input_dir):
    print usage
    sys.exit()

  main_workdir = options.main_workdir
  input_dir = options.input_dir

  # redefine main_workdir as an absolute path (if not defined in such form already)
  if not re.search("^/", main_workdir):
    main_workdir = os.path.join(os.getcwd(),main_workdir)

  # create the main working directory
  if not os.path.exists(main_workdir):
    os.mkdir(main_workdir)
  else:
    print 'Main working directory already exists. Aborting'
    sys.exit()

  # copy the Analysis python script
  shutil.copyfile(options.py_file,os.path.join(main_workdir,'analysis.py'))

  jobs_dir = os.path.join(main_workdir,'jobs')
  os.mkdir(jobs_dir)
  output_dir = os.path.join(main_workdir,'output')
  os.mkdir(os.path.join(main_workdir,'output'))

  filelist = []
  process_input_dir(input_dir, options.match, filelist)

  # create and submit jobs (one input file per job)
  nfiles = int(len(filelist)*float(options.fraction))

  for ifile in range(0,nfiles):

    input_file = 'root://eoscms.cern.ch/' + filelist[ifile]
    output_filename = 'histos_mjj_' + str(ifile) + '.root'
    shell_script = 'job_' + str(ifile) + '.sh'

    ## create Bash script
    bash_script = open(os.path.join(jobs_dir,shell_script),'w')
    bash_script_content = re.sub('MAIN_WORKDIR',main_workdir,bash_template)
    bash_script_content = re.sub('INPUT_FILE',input_file,bash_script_content)
    bash_script_content = re.sub('OUTPUT_FILENAME',output_filename,bash_script_content)
    bash_script.write(bash_script_content)
    bash_script.close()

    if(not options.no_submission):
      cmd = 'bsub -q ' + options.queue + ' -o ' + os.path.join(output_dir,'job_' + str(ifile) + '.log') + ' source ' + os.path.join(jobs_dir,shell_script)
      print cmd
      os.system(cmd)

if __name__ == "__main__":
  main()

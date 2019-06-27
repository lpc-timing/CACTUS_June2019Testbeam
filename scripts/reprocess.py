#!/usr/bin/python

import os
import datetime
import time
import subprocess
import glob
import sys



if len(sys.argv) < 2:
    print "Usage: python reprocess.py [run number]\n"
    exit()

run=sys.argv[1]

print "Processing Run "+run+"\n"


#Define Data Directories
trackDir="/eos/uscms/store/user/cmstestbeam/2019_04_April_CMSTiming/Tracks/"
scopeRawDir="/eos/uscms/store/user/cmstestbeam/2019_04_April_CMSTiming/KeySightScope/RawData/"
scopeConversionDir="/eos/uscms/store/user/cmstestbeam/2019_04_April_CMSTiming/KeySightScope/RecoData/ConversionRECO/"
scopeRecoDir="/eos/uscms/store/user/cmstestbeam/2019_04_April_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v6/"


print "\n##########################################"
print   "## Check for input files\n"
print   "##########################################\n"
if not os.path.exists(trackDir+"Run"+run+"_CMSTiming_FastTriggerStream_converted.root"):
    print "Tracker input file " + trackDir+"Run"+run+"_CMSTiming_FastTriggerStream_converted.root" + " does not exist\n"
    exit()
if not os.path.exists(scopeRawDir+"Wavenewscope_CH1_"+run+".bin"):
    print "Scope Raw Data File " + scopeRawDir+"Wavenewscope_CH1_"+run+".bin" + " does not exist\n"
    exit()
if not os.path.exists(scopeRawDir+"Wavenewscope_CH2_"+run+".bin"):
    print "Scope Raw Data File " + scopeRawDir+"Wavenewscope_CH2_"+run+".bin" + " does not exist\n"
    exit()
if not os.path.exists(scopeRawDir+"Wavenewscope_CH3_"+run+".bin"):
    print "Scope Raw Data File " + scopeRawDir+"Wavenewscope_CH3_"+run+".bin" + " does not exist\n"
    exit()
if not os.path.exists(scopeRawDir+"Wavenewscope_CH4_"+run+".bin"):
    print "Scope Raw Data File " + scopeRawDir+"Wavenewscope_CH4_"+run+".bin" + " does not exist\n"
    exit()


print "\n##########################################"
print   "## Run Scope Conversion\n"
print   "##########################################\n"

if not os.path.exists(scopeConversionDir+"run_scope"+run+".root"):
    print "Scope Conversion file does not exist. Run Scope conversion\n";
    print "python /uscms/home/sxie/CMSSW_Timing/src/TimingDAQ_fast_reco_withTOT/ETL_Agilent_MSO-X-92004A/Reconstruction/conversion_bin_fast.py --Run "+run
    os.system("python /uscms/home/sxie/CMSSW_Timing/src/TimingDAQ_fast_reco_withTOT/ETL_Agilent_MSO-X-92004A/Reconstruction/conversion_bin_fast.py --Run " + run)
else :
    print "Scope Conversion file already exists. Do not need to run scope conversion\n";


print "\n##########################################"
print   "## Run Reconstruction\n"
print   "##########################################\n"
if not os.path.exists(scopeRecoDir+"run_scope"+run+"_converted.root"):
    print "Reco file does not exist. Run Scope reconstruction\n";
    print "./NetScopeStandaloneDat2Root --config_file=/uscms/home/sxie/CMSSW_Timing/src/TimingDAQ_fast_reco_withTOT/config/KeySightScope_v3_withTOT.config --input_file="+scopeConversionDir+"run_scope"+run+".root"+" --output_file=" + scopeRecoDir+"run_scope"+run+"_converted.root" + " --save_meas --pixel_input_file="+trackDir+"Run"+run+"_CMSTiming_FastTriggerStream_converted.root"
    os.system("./NetScopeStandaloneDat2Root --config_file=/uscms/home/sxie/CMSSW_Timing/src/TimingDAQ_fast_reco_withTOT/config/KeySightScope_v3_withTOT.config --input_file="+scopeConversionDir+"run_scope"+run+".root"+" --output_file=" + scopeRecoDir+"run_scope"+run+"_converted.root" + " --save_meas --pixel_input_file="+trackDir+"Run"+run+"_CMSTiming_FastTriggerStream_converted.root")

else :
    print "Reco file already exists. Do not need to run reconstruction\n"


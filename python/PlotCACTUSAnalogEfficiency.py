from ROOT import TFile,TTree,TCanvas,TH1F,TH2F,TLatex,TMath,TEfficiency,TGraphAsymmErrors
import os
import EfficiencyUtils


inputfile_5_3 = "/eos/uscms/store/user/cmstestbeam/2019_04_April_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v6_CACTUSSkim/Completed/Data_CACTUSAnalog_Pixel5_3_16216-16263.root"
inputfile_5_4 = "/eos/uscms/store/user/cmstestbeam/2019_04_April_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v6_CACTUSSkim/Completed/Data_CACTUSAnalog_Pixel5_4_17063-17362.root"
inputfile_5_10 = "/eos/uscms/store/user/cmstestbeam/2019_04_April_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v6_CACTUSSkim/Completed/Data_CACTUSAnalog_Pixel5_10_16725-17039.root"

if not os.path.exists(inputfile_5_3):
    print "input file "+inputfile_5_3+" does not exist"
    exit()
if not os.path.exists(inputfile_5_4):
    print "input file "+inputfile_5_4+" does not exist"
    exit()
if not os.path.exists(inputfile_5_10):
    print "input file "+inputfile_5_10+" does not exist"
    exit()




file_5_3 = TFile(inputfile_5_3)
tree_5_3 = file_5_3.Get("pulse")
file_5_4 = TFile(inputfile_5_4)
tree_5_4 = file_5_4.Get("pulse")
file_5_10 = TFile(inputfile_5_10)
tree_5_10 = file_5_10.Get("pulse")

timeCut = " && (t_peak[3] - t_peak[0])*1e9 > 6 && !((t_peak[3] - t_peak[0])*1e9  < 16) "
ampCut = " && amp[3] > 15"

##########################
#2D Efficiency 
##########################
den = TH2F("den",";x;y",20,19,21,20,23,25)
num = TH2F("num",";x;y",20,19,21,20,23,25)
tree_5_3.Draw("y_dut[2]:x_dut[2]>>den","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0"+timeCut,"colz")
tree_5_3.Draw("y_dut[2]:x_dut[2]>>num","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0"+timeCut+ampCut,"colz")

EfficiencyUtils.Plot2DEfficiency(num, den, "CACTUSAnalog_Pixel5_3_EfficiencyVsXY", "CACTUS Pixel (5,3) Analog", "X [mm]", 19.0, 21.0, "Y [mm]", 23.0, 25.0, -0.001, 1.0)


##########################
#1D Efficiency Vs X
##########################

den_X = TH1F("den_X",";X [mm];Number of Events",20,19,21)
num_X = TH1F("num_X",";X [mm];Number of Events",20,19,21)
tree_5_3.Draw("x_dut[2]>>den_X","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0 && y_dut[2] > 23.52 && y_dut[2] < 23.98"+timeCut,"")
tree_5_3.Draw("x_dut[2]>>num_X","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0 && y_dut[2] > 23.52 && y_dut[2] < 23.98"+timeCut+ampCut,"")


EfficiencyUtils.Plot1DEfficiency(num_X,den_X,"CACTUSAnalog_Pixel5_3_EfficiencyVsX","CACTUS Pixel (5,3) Analog","X [mm]",19.0,21.0)



##########################
#1D Efficiency Vs Y
##########################
den_Y = TH1F("den_Y",";X [mm];Number of Events",20,23,25)
num_Y = TH1F("num_Y",";X [mm];Number of Events",20,23,25)
tree_5_3.Draw("y_dut[2]>>den_Y","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0 && x_dut[2] > 19.52 && x_dut[2] < 20.45"+timeCut,"")
tree_5_3.Draw("y_dut[2]>>num_Y","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0 && x_dut[2] > 19.52 && x_dut[2] < 20.45"+timeCut+ampCut,"")

EfficiencyUtils.Plot1DEfficiency(num_Y,den_Y,"CACTUSAnalog_Pixel5_3_EfficiencyVsY","CACTUS Pixel (5,3) Analog","Y [mm]",23.0,25.0)


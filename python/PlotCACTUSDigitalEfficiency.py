from ROOT import TFile,TTree,TCanvas,TH1F,TH2F,TLatex,TMath,TEfficiency,TGraphAsymmErrors
import os
import EfficiencyUtils


inputfile = "/eos/uscms/store/user/cmstestbeam/2019_04_April_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v6_CACTUSSkim/Completed/Data_CACTUSDigital_HighThreshold_16428-16454.root"

if not os.path.exists(inputfile):
    print "input file "+inputfile+" does not exist"
    exit()


file = TFile(inputfile)
tree = file.Get("pulse")

#c = TCanvas("cv","cv",800,800)

##########################
#2D Efficiency 
##########################
den = TH2F("den",";x;y",20,19,21,20,23,25)
num = TH2F("num",";x;y",20,19,21,20,23,25)
tree.Draw("y_dut[2]:x_dut[2]>>den","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0","colz")
tree.Draw("y_dut[2]:x_dut[2]>>num","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0 && amp[3] > 200 ","colz")

EfficiencyUtils.Plot2DEfficiency(num, den, "CACTUSEfficiencyVsXY", "CACTUS Pixel (5,3) Digital", "X [mm]", 19.0, 21.0, "Y [mm]", 23.0, 25.0, -0.001, 0.25)


##########################
#1D Efficiency Vs X
##########################

den_X = TH1F("den_X",";X [mm];Number of Events",20,19,21)
num_X = TH1F("num_X",";X [mm];Number of Events",20,19,21)
tree.Draw("x_dut[2]>>den_X","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0 && y_dut[2] > 23.52 && y_dut[2] < 23.98","colz")
tree.Draw("x_dut[2]>>num_X","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0 && y_dut[2] > 23.52 && y_dut[2] < 23.98 && amp[3] > 200 ","colz")


EfficiencyUtils.Plot1DEfficiency(num_X,den_X,"CACTUSEfficiencyVsX","CACTUS Pixel (5,3) Digital","X [mm]",19.0,21.0)



##########################
#1D Efficiency Vs Y
##########################
den_Y = TH1F("den_Y",";X [mm];Number of Events",20,23,25)
num_Y = TH1F("num_Y",";X [mm];Number of Events",20,23,25)
tree.Draw("y_dut[2]>>den_Y","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0 && x_dut[2] > 19.52 && x_dut[2] < 20.45","colz")
tree.Draw("y_dut[2]>>num_Y","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0 && x_dut[2] > 19.52 && x_dut[2] < 20.45 && amp[3] > 200 ","colz")

EfficiencyUtils.Plot1DEfficiency(num_Y,den_Y,"CACTUSEfficiencyVsY","CACTUS Pixel (5,3) Digital","Y [mm]",23.0,25.0)


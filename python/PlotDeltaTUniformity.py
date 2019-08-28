from ROOT import TFile,TTree,TCanvas,TH1F,TH2F,TLatex,TMath,TEfficiency,TGraphErrors
import os
import array
import sys

##############################################################################
#Command line deltaT  and deriving the TOT corrections
##############################################################################
#DeltaT
#pulse->Draw("1e9*(t0CFD_50[3] - LP2_50[0]) >> h(100,3,13)","amp[3]>200 && amp[0] > 100 && amp[0] < 700 && LP2_50[0] != 0 && t0CFD_50[3] != 0 ")
# some pulses did not get a proper timestamp calculated and it defaulted to a value of 0. we remove those cases from the analysis

#TOT Correction
#pulse->Draw("1e9*(t0CFD_50[3] - LP2_50[0]) : totCFD_50[3]*1e9 >> hh(100,50,200,100,0,20)","amp[3]>200 && amp[0] > 100 && amp[0] < 700 && L(Long64_t) 1139& t0CFD_50[3] != 0 ","colz")
#hh->ProfileX()->Draw()

#With TOT correction: get 550ps resolution
#pulse->Draw("1e9*(t0CFD_50[3] - LP2_50[0]) - (16.7292 -0.0799991*totCFD_50[3]*1e9) >> h1(100,-10,10)","amp[3]>200 && amp[0] > 100 && amp[0] < 700 && LP2_50[0] != 0 && t0CFD_50[3] != 0 ","")


##############################################################################
#Derived the TOT corrections for the CACTUS signal 
##############################################################################

#For data: timingoptimized_lowThreshold
#TOT Correction
#pulse->Draw("1e9*(t0CFD_50[3] - LP2_50[0]) : totCFD_50[3]*1e9 >> hh(100,50,200,100,0,20)","amp[3]>200 && amp[0] > 100 && amp[0] < 700 &&  LP2_50[0] != 0 && t0CFD_50[3] != 0 ","colz")
#hh->ProfileX()->Draw()
#With TOT correction: get 550ps resolution
#pulse->Draw("1e9*(t0CFD_50[3] - LP2_50[0]) - (16.7292 -0.0799991*totCFD_50[3]*1e9) >> h1(100,-10,10)","amp[3]>200 && amp[0] > 100 && amp[0] < 700 && LP2_50[0] != 0 && t0CFD_50[3] != 0 ","")


#For data: timingoptimized_highThreshold
#TOT Correction
#pulse->Draw("1e9*(t0CFD_50[3] - LP2_50[0]) : totCFD_50[3]*1e9 >> hh(100,50,200,100,0,20)","amp[3]>200 && amp[0] > 100 && amp[0] < 700 &&  LP2_50[0] != 0 && t0CFD_50[3] != 0","colz")
#hh->ProfileX()->Draw()
#With TOT correction: get 580ps resolution
#pulse->Draw("1e9*(t0CFD_50[3] - LP2_50[0]) - (20.143-0.108262*totCFD_50[3]*1e9)  >> hh(100,-10,10)","amp[3]>200 && amp[0] > 100 && amp[0] < 700 &&  LP2_50[0] != 0 && t0CFD_50[3] != 0","")
# Here we only got 70 events -> so not much data to deal with...

#For data: lowThreshold
#TOT Correction
#pulse->Draw("1e9*(t0CFD_50[3] - LP2_50[0]) : totCFD_50[3]*1e9 >> hh(100,50,200,100,0,20)","amp[3]>200 && amp[0] > 100 && amp[0] < 700 &&  LP2_50[0] != 0 && t0CFD_50[3] != 0","colz")
#hh->ProfileX()->Draw()
#With TOT correction: get 840ps resolution
#pulse->Draw("1e9*(t0CFD_50[3] - LP2_50[0]) - (totCFD_50[3]*1e9<=128)*(8.5)- (totCFD_50[3]*1e9>128)*(21.2076-0.0985751*totCFD_50[3]*1e9) >> hh(100,-10,10)","amp[3]>200 && amp[0] > 100 && amp[0] < 700 &&  LP2_50[0] != 0 && t0CFD_50[3] != 0","colz")


#For data: highThreshold
#TOT Correction
#pulse->Draw("1e9*(t0CFD_50[3] - LP2_50[0]) : totCFD_50[3]*1e9 >> hh(100,50,200,100,0,20)","amp[3]>200 && amp[0] > 100 && amp[0] < 700 &&  LP2_50[0] != 0 && t0CFD_50[3] != 0","colz")
#hh->ProfileX()->Draw()
#With TOT correction: get 720ps resolution
#pulse->Draw("1e9*(t0CFD_50[3] - LP2_50[0]) - (totCFD_50[3]*1e9  <= 120)*8.5 - (totCFD_50[3]*1e9  > 120)*(20.9304-0.101498*totCFD_50[3]*1e9)  >> hh(100,-10,10)","amp[3]>200 && amp[0] > 100 && amp[0] < 700 &&  LP2_50[0] != 0 && t0CFD_50[3] != 0","")


inputfile_timingoptimized_lowThreshold = "/eos/uscms/store/user/cmstestbeam/2019_04_April_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v6_CACTUSSkim/Completed/Data_CACTUSDigital_TimingOptimized_LowThreshold_16517-16711.root"
inputfile_timingoptimized_highThreshold = "/eos/uscms/store/user/cmstestbeam/2019_04_April_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v6_CACTUSSkim/Completed/Data_CACTUSDigital_TimingOptimized_HighTreshold_16492-16516.root"
inputfile_lowThreshold = "/eos/uscms/store/user/cmstestbeam/2019_04_April_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v6_CACTUSSkim/Completed/Data_CACTUSDigital_LowThreshold_16467-16488.root"
inputfile_highThreshold = "/eos/uscms/store/user/cmstestbeam/2019_04_April_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v6_CACTUSSkim/Completed/Data_CACTUSDigital_HighThreshold_16428-16454.root"
inputfile = ""
outputLabel = ""
pixelName = ""

if (len(sys.argv) < 2):
    print "Please give an argument to select the dataset: (1) Pixel 5_3 data , (2) Pixel 5_4 data, (3) Pixel 5_10 data."
    exit()

xMin = 19
xMax = 21
yMin = 22.5
yMax = 24.5
xPositionSelection = " && x_dut[2] > 19.55 && x_dut[2] < 20.45 "
yPositionSelection = " && y_dut[2] > 23.55 && y_dut[2] < 23.95 "
pixelName = "(5,3)"
deltaTDrawCommand = ""
selectionCommand = "&& amp[3]>200 && amp[0] > 100 && amp[0] < 700 &&  LP2_50[0] != 0 && t0CFD_50[3] != 0 "

if (sys.argv[1] == "1"):
    inputfile = inputfile_timingoptimized_lowThreshold
    outputLabel = "_Pixel_5_3_TimingOptimizedLowThreshold"
    deltaTDrawCommand = "1e9*(t0CFD_50[3] - LP2_50[0]) - (16.7292 -0.0799991*totCFD_50[3]*1e9)"

if (sys.argv[1] == "2"):
    inputfile = inputfile_timingoptimized_highThreshold
    outputLabel = "_Pixel_5_3_TimingOptimizedHighThreshold"
    deltaTDrawCommand = "1e9*(t0CFD_50[3] - LP2_50[0]) - (20.143-0.108262*totCFD_50[3]*1e9)"

if (sys.argv[1] == "3"):
    inputfile = inputfile_lowThreshold
    outputLabel = "_Pixel_5_3_LowThreshold"
    deltaTDrawCommand = "1e9*(t0CFD_50[3] - LP2_50[0]) - (totCFD_50[3]*1e9<=128)*(8.5)- (totCFD_50[3]*1e9>128)*(21.2076-0.0985751*totCFD_50[3]*1e9)"

if (sys.argv[1] == "4"):
    inputfile = inputfile_highThreshold
    outputLabel = "_Pixel_5_3_HighThreshold"
    deltaTDrawCommand = "1e9*(t0CFD_50[3] - LP2_50[0]) - (totCFD_50[3]*1e9  <= 120)*8.5 - (totCFD_50[3]*1e9  > 120)*(20.9304-0.101498*totCFD_50[3]*1e9)"


if not os.path.exists(inputfile):
    print "input file "+inputfile+" does not exist"
    exit()


file = TFile(inputfile, "READ")
tree = file.Get("pulse")

c = TCanvas("cv","cv",800,800)







##########################
#1D MPV Vs X
##########################
xLeftBoundary = xMin
xRightBoundary = xMax
xBinWidth = 0.1
xNBins = int((xRightBoundary - xLeftBoundary)/xBinWidth)

tmpHist = TH1F("tmp",";X [mm];NEvt", xNBins, xLeftBoundary, xRightBoundary)
tmpHist2D = TH2F("tmpHist2D",";X [mm];Amplitude [mV]; NEvt", xNBins, xLeftBoundary, xRightBoundary, 100, -10, 10)

tree.Draw(deltaTDrawCommand + ":x_dut[2] >> tmpHist2D","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0 " + yPositionSelection + xPositionSelection + selectionCommand,"colz")

x = list()
xErr = list()
dTMean = list()
dTMeanErr = list()
nbins = tmpHist2D.GetXaxis().GetNbins()

for b in range(1,tmpHist2D.GetXaxis().GetNbins()+1):
    projectionHist = tmpHist2D.ProjectionY("proj"+str(b), b,b)

    x.append( tmpHist2D.GetXaxis().GetBinCenter(b))
    xErr.append( tmpHist2D.GetXaxis().GetBinCenter(b) - tmpHist2D.GetXaxis().GetBinLowEdge(b))
    tmpDeltaTMean = -10
    tmpDeltaTMeanErr = 0

    #skip bins with too few events
    if (projectionHist.Integral() > 20) : 
        
        tmpDeltaTMean = projectionHist.GetMean()
        tmpDeltaTMeanErr = projectionHist.GetMeanError()
 
    dTMean.append(tmpDeltaTMean)
    dTMeanErr.append(tmpDeltaTMeanErr)


xArr = array.array('f',x)
xErrArr = array.array('f',xErr)
yArr = array.array('f',dTMean)
yErrArr = array.array('f',dTMeanErr)

effGraph = TGraphErrors(nbins, xArr, yArr, xErrArr, yErrArr );
effGraph.Draw("APE")
effGraph.SetTitle("")
effGraph.GetXaxis().SetTitle("X [mm]")
effGraph.GetXaxis().SetTitleSize(0.05)
effGraph.GetXaxis().SetTitleOffset(0.90)
effGraph.GetXaxis().SetLabelSize(0.03)
#effGraph.GetXaxis().SetRangeUser(23.0,25.0)
effGraph.GetYaxis().SetTitle("Mean #Delta t [ns]")
effGraph.GetYaxis().SetTitleSize(0.05)
effGraph.GetYaxis().SetTitleOffset(0.92)
effGraph.GetYaxis().SetLabelSize(0.03)
effGraph.GetYaxis().SetRangeUser(-2,2)

title = TLatex()
title.SetTextSize(0.05);
#title.SetTextAlign(13);  
title.DrawLatexNDC(.2,.93,"CACTUS Pixel "+pixelName+" Analog");
c.Update()
c.SaveAs("CACTUS_DeltaTMeanVsX" + outputLabel + ".gif")





##########################
#1D MPV Vs Y
##########################
yLeftBoundary = yMin
yRightBoundary = yMax
yBinWidth = 0.1
yNBins = int((yRightBoundary - yLeftBoundary)/yBinWidth)


tmpHist2D = TH2F("tmpHist2D",";Y [mm];Amplitude [mV]; NEvt", yNBins, yLeftBoundary, yRightBoundary, 100, -10, 10)

tree.Draw(deltaTDrawCommand + ":y_dut[2] >> tmpHist2D","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0 " + yPositionSelection + xPositionSelection + selectionCommand,"colz")

y = list()
yErr = list()
dTMean = list()
dTMeanErr = list()
nbins = tmpHist2D.GetXaxis().GetNbins()

for b in range(1,tmpHist2D.GetXaxis().GetNbins()+1):
    projectionHist = tmpHist2D.ProjectionY("proj"+str(b), b,b)

    y.append( tmpHist2D.GetXaxis().GetBinCenter(b))
    yErr.append( tmpHist2D.GetXaxis().GetBinCenter(b) - tmpHist2D.GetXaxis().GetBinLowEdge(b))
    tmpDeltaTMean = -10
    tmpDeltaTMeanErr = 0

    #skip bins with too few events
    if (projectionHist.Integral() > 20) : 

        tmpDeltaTMean = projectionHist.GetMean()
        tmpDeltaTMeanErr = projectionHist.GetMeanError()
 
    dTMean.append(tmpDeltaTMean)
    dTMeanErr.append(tmpDeltaTMeanErr)


xArr = array.array('f',x)
xErrArr = array.array('f',xErr)
yArr = array.array('f',dTMean)
yErrArr = array.array('f',dTMeanErr)

effGraph = TGraphErrors(nbins, xArr, yArr, xErrArr, yErrArr );
effGraph.Draw("APE")
effGraph.SetTitle("")
effGraph.GetXaxis().SetTitle("Y [mm]")
effGraph.GetXaxis().SetTitleSize(0.05)
effGraph.GetXaxis().SetTitleOffset(0.90)
effGraph.GetXaxis().SetLabelSize(0.03)
effGraph.GetXaxis().SetRangeUser(23.0,25.0)
effGraph.GetYaxis().SetTitle("Mean #Delta t [ns]")
effGraph.GetYaxis().SetTitleSize(0.05)
effGraph.GetYaxis().SetTitleOffset(0.92)
effGraph.GetYaxis().SetLabelSize(0.03)
effGraph.GetYaxis().SetRangeUser(-2,2)

title = TLatex()
title.SetTextSize(0.05);
#title.SetTextAlign(13);  
title.DrawLatexNDC(.2,.93,"CACTUS Pixel "+pixelName+" Analog");
c.Update()
c.SaveAs("CACTUS_DeltaTMeanVsY" + outputLabel + ".gif")







file.Close()

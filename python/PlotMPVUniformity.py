from ROOT import TFile,TTree,TCanvas,TH1F,TH2F,TLatex,TMath,TEfficiency,TGraphErrors
import os
import array


inputfile = "/eos/uscms/store/user/cmstestbeam/2019_04_April_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v6_CACTUSSkim/Completed/Data_CACTUSAnalog_HighGain_16719-16722+17040-17062.root"

if not os.path.exists(inputfile):
    print "input file "+inputfile+" does not exist"
    exit()


file = TFile(inputfile, "READ")
tree = file.Get("pulse")

c = TCanvas("cv","cv",800,800)

#Signal amplitude 
#tree.Draw("amp[3] >> h3(50,0,100) ","(y_dut[2] > 23.55 && y_dut[2] < 23.95 && x_dut[2] > 19.6 && x_dut[2] < 20.4) && amp[0] > 150 && amp[0] < 600 && ( (t_peak[3] - t_peak[0])*1e9 > 0 && (t_peak[3] - t_peak[0])*1e9 < 25)","colz")



##########################
#1D MPV Vs X
##########################
xLeftBoundary = 19
xRightBoundary = 21
xBinWidth = 0.1
xNBins = int((xRightBoundary - xLeftBoundary)/xBinWidth)

tmpHist = TH1F("tmp",";X [mm];NEvt", xNBins, xLeftBoundary, xRightBoundary)
tmpHist2D = TH2F("tmpHist2D",";X [mm];Amplitude [mV]; NEvt", xNBins, xLeftBoundary, xRightBoundary, 50, 0, 100)
#xBinEdges = list()
#xBinEdges.append(xLeftBoundary)
#for i in range(1,(xRightBoundary - xLeftBoundary)/xBinWidth + 1):
#    xBinEdges.append(xLeftBoundary + i*xBinWidth)

tree.Draw("amp[3]:x_dut[2] >> tmpHist2D","(y_dut[2] > 23.55 && y_dut[2] < 23.95 && x_dut[2] > 19.5 && x_dut[2] < 20.5) && amp[0] > 150 && amp[0] < 600 && ( (t_peak[3] - t_peak[0])*1e9 > 0 && (t_peak[3] - t_peak[0])*1e9 < 25)","colz")

x = list()
xErr = list()
mpv = list()
mpvErr = list()
nbins = tmpHist2D.GetXaxis().GetNbins()

for b in range(1,tmpHist2D.GetXaxis().GetNbins()+1):
    projectionHist = tmpHist2D.ProjectionY("proj"+str(b), b,b)

    x.append( tmpHist2D.GetXaxis().GetBinCenter(b))
    xErr.append( tmpHist2D.GetXaxis().GetBinCenter(b) - tmpHist2D.GetXaxis().GetBinLowEdge(b))
    tmpMPV = -1
    tmpMPVErr = 0

    #skip bins with too few events
    if (projectionHist.Integral() > 100) : 

        fitresult = projectionHist.Fit("landau","S")
        tmpMPV = fitresult.Parameter(1)
        tmpMPVErr = fitresult.ParError(1)
 
    #rint "bin "+str(b)+" X in " + str(tmpHist2D.GetXaxis().GetBinLowEdge(b)) + " - " + str(tmpHist2D.GetXaxis().GetBinUpEdge(b)) + " : " + str(projectionHist.Integral())
    #rint str(mpv)+ " +/- " + str(mpvErr)

    mpv.append(tmpMPV)
    mpvErr.append(tmpMPVErr)


xArr = array.array('f',x)
xErrArr = array.array('f',xErr)
yArr = array.array('f',mpv)
yErrArr = array.array('f',mpvErr)

effGraph = TGraphErrors(nbins, xArr, yArr, xErrArr, yErrArr );
effGraph.Draw("APE")
effGraph.SetTitle("")
effGraph.GetXaxis().SetTitle("X [mm]")
effGraph.GetXaxis().SetTitleSize(0.05)
effGraph.GetXaxis().SetTitleOffset(0.90)
effGraph.GetXaxis().SetLabelSize(0.03)
#effGraph.GetXaxis().SetRangeUser(23.0,25.0)
effGraph.GetYaxis().SetTitle("Amplitude MPV [mV]")
effGraph.GetYaxis().SetTitleSize(0.05)
effGraph.GetYaxis().SetTitleOffset(0.92)
effGraph.GetYaxis().SetLabelSize(0.03)
effGraph.GetYaxis().SetRangeUser(15.0,25.0)

title = TLatex()
title.SetTextSize(0.05);
#title.SetTextAlign(13);  
title.DrawLatexNDC(.2,.93,"CACTUS Pixel (5,3) Analog");
c.Update()
c.SaveAs("CACTUS_MPVVsX.gif")





##########################
#1D MPV Vs Y
##########################
yLeftBoundary = 23.0
yRightBoundary = 25.0
yBinWidth = 0.1
yNBins = int((yRightBoundary - yLeftBoundary)/yBinWidth)


tmpHist2D = TH2F("tmpHist2D",";Y [mm];Amplitude [mV]; NEvt", yNBins, yLeftBoundary, yRightBoundary, 50, 0, 100)

tree.Draw("amp[3]:y_dut[2] >> tmpHist2D","(y_dut[2] > 23.50 && y_dut[2] < 24.0 && x_dut[2] > 19.6 && x_dut[2] < 20.4) && amp[0] > 150 && amp[0] < 600 && ( (t_peak[3] - t_peak[0])*1e9 > 0 && (t_peak[3] - t_peak[0])*1e9 < 25)","colz")

y = list()
yErr = list()
mpv = list()
mpvErr = list()
nbins = tmpHist2D.GetXaxis().GetNbins()

for b in range(1,tmpHist2D.GetXaxis().GetNbins()+1):
    projectionHist = tmpHist2D.ProjectionY("proj"+str(b), b,b)

    y.append( tmpHist2D.GetXaxis().GetBinCenter(b))
    yErr.append( tmpHist2D.GetXaxis().GetBinCenter(b) - tmpHist2D.GetXaxis().GetBinLowEdge(b))
    tmpMPV = -1
    tmpMPVErr = 0

    #skip bins with too few events
    if (projectionHist.Integral() > 100) : 

        fitresult = projectionHist.Fit("landau","S")
        tmpMPV = fitresult.Parameter(1)
        tmpMPVErr = fitresult.ParError(1)
 
    mpv.append(tmpMPV)
    mpvErr.append(tmpMPVErr)


xArr = array.array('f',x)
xErrArr = array.array('f',xErr)
yArr = array.array('f',mpv)
yErrArr = array.array('f',mpvErr)

effGraph = TGraphErrors(nbins, xArr, yArr, xErrArr, yErrArr );
effGraph.Draw("APE")
effGraph.SetTitle("")
effGraph.GetXaxis().SetTitle("Y [mm]")
effGraph.GetXaxis().SetTitleSize(0.05)
effGraph.GetXaxis().SetTitleOffset(0.90)
effGraph.GetXaxis().SetLabelSize(0.03)
effGraph.GetXaxis().SetRangeUser(23.0,25.0)
effGraph.GetYaxis().SetTitle("Amplitude MPV [mV]")
effGraph.GetYaxis().SetTitleSize(0.05)
effGraph.GetYaxis().SetTitleOffset(0.92)
effGraph.GetYaxis().SetLabelSize(0.03)
effGraph.GetYaxis().SetRangeUser(15.0,25.0)

title = TLatex()
title.SetTextSize(0.05);
#title.SetTextAlign(13);  
title.DrawLatexNDC(.2,.93,"CACTUS Pixel (5,3) Analog");
c.Update()
c.SaveAs("CACTUS_MPVVsY.gif")



file.Close()

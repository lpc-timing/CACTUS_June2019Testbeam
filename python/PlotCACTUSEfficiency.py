from ROOT import TFile,TTree,TCanvas,TH1F,TH2F,TLatex,TMath,TEfficiency,TGraphAsymmErrors
import os
import array


inputfile = "/eos/uscms/store/user/cmstestbeam/2019_04_April_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v6_CACTUSSkim/Completed/Data_CACTUSDigital_HighThreshold_16428-16454.root"

if not os.path.exists(inputfile):
    print "input file "+inputfile+" does not exist"
    exit()


file = TFile(inputfile)
tree = file.Get("pulse")

c = TCanvas("cv","cv",800,800)

##########################
#2D Efficiency 
##########################
den = TH2F("den",";x;y",20,19,21,20,23,25)
num = TH2F("num",";x;y",20,19,21,20,23,25)
tree.Draw("y_dut[2]:x_dut[2]>>den","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0","colz")
tree.Draw("y_dut[2]:x_dut[2]>>num","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0 && amp[3] > 200 ","colz")

num.Divide(den)

num.Draw("colz")
num.SetMaximum(0.25)
num.SetMinimum(-0.001)
num.GetZaxis().SetTitle("Efficiency")
num.GetZaxis().SetTitleSize(0.05)
num.GetZaxis().SetTitleOffset(1.25)
num.Draw("colz")
num.SetStats(0)
num.GetXaxis().SetTitle("X [mm]")
num.GetXaxis().SetTitleSize(0.05)
num.GetXaxis().SetTitleOffset(0.90)
num.GetXaxis().SetLabelSize(0.03)
num.GetYaxis().SetTitle("Y [mm]")
num.GetYaxis().SetTitleSize(0.05)
num.GetYaxis().SetTitleOffset(1.05)
num.GetYaxis().SetLabelSize(0.03)
c.SetRightMargin(0.18)
c.SetLeftMargin(0.12)

title = TLatex()
title.SetTextSize(0.05);
#title.SetTextAlign(13);  
title.DrawLatexNDC(.2,.93,"CACTUS Pixel (5,3) Digital");
c.Update()
c.SaveAs("CACTUSEfficiency.gif")

##########################
#1D Efficiency Vs X
##########################
den_X = TH1F("den_X",";X [mm];Number of Events",20,19,21)
num_X = TH1F("num_X",";X [mm];Number of Events",20,19,21)
tree.Draw("x_dut[2]>>den_X","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0 && y_dut[2] > 23.52 && y_dut[2] < 23.98","colz")
tree.Draw("x_dut[2]>>num_X","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0 && y_dut[2] > 23.52 && y_dut[2] < 23.98 && amp[3] > 200 ","colz")



nbins = num_X.GetXaxis().GetNbins()
x = list()
y = list()
xErrLow = list()
xErrHigh = list()
yErrLow = list()
yErrHigh = list()

#effHist = num.Clone("effHist")
#for i in range(1,effHist.GetAxis().GetNbins()):
#    r = num_X.GetBinContent(i) / den_X.GetBinContent(i)
#    rErr = r * sqrt(pow(num_X.GetBinError(i) / num_X.GetBinContent(i),2) + pow(den_X.GetBinError(i) / den_X.GetBinContent(i),2))
#    effHist.SetBinContent(i, r)
#    effHist.SetBinError(i, rErr)



for b in range(1,nbins):

    xtemp = num_X.GetXaxis().GetBinCenter(b+1)
    xerrlow =  num_X.GetXaxis().GetBinCenter(b+1) - num_X.GetXaxis().GetBinLowEdge(b+1)  
    xerrhigh = num_X.GetXaxis().GetBinUpEdge(b+1) - num_X.GetXaxis().GetBinCenter(b+1)  

    ratio = 0
    errLow = 0
    errHigh = 0

    n1 = int(num_X.GetBinContent(b+1));
    n2 = int(den_X.GetBinContent(b+1));
    print "numerator: " + str(n1) + " and denominator: " + str(n2)
    if (n1 > n2):
        n1 = n2;

    if (n2>0) :
      ratio = float(n1)/float(n2);
      if (ratio > 1) :
          ratio = 1;
      errLow = ratio - TEfficiency.ClopperPearson(n2, n1, 0.68269, False);
      errHigh = TEfficiency.ClopperPearson(n2, n1, 0.68269, True) - ratio;
    

    print " done bin " + str(b) + " " + str(xtemp) + " : " + str(n1) + "(" + str(num_X.GetBinContent(b+1)) + ")" + " / " + str(n2) + "(" + str(den_X.GetBinContent(b+1)) + ")" + " = " + str(ratio) + " " + str(errLow) + " " + str(errHigh)
    ytemp = ratio
    yerrlowtemp = errLow
    yerrhightemp = errHigh
    
    #if((yerrhightemp >= .5*ytemp) | (yerrlowtemp >= .5*ytemp)) continue; 
  
    print "x: " + str(xtemp) + " and y: " + str(ytemp)

    x.append(xtemp);  
    y.append(ytemp); 
    xErrLow.append(xerrlow);
    xErrHigh.append(xerrhigh);
    yErrLow.append(yerrlowtemp);
    yErrHigh.append(yerrhightemp);
    

xArr = array.array('f',x)
yArr = array.array('f',y)
xErrLowArr = array.array('f',xErrLow)
xErrHighArr = array.array('f',xErrHigh)
yErrLowArr = array.array('f',yErrLow)
yErrHighArr = array.array('f',yErrHigh)

effGraph = TGraphAsymmErrors(nbins, xArr, yArr, xErrLowArr, xErrHighArr, yErrLowArr,yErrHighArr );
effGraph.Draw("APE")
effGraph.SetTitle("")
effGraph.GetXaxis().SetTitle("X [mm]")
effGraph.GetXaxis().SetTitleSize(0.05)
effGraph.GetXaxis().SetTitleOffset(0.90)
effGraph.GetXaxis().SetLabelSize(0.03)
effGraph.GetXaxis().SetRangeUser(19.0,21.0)
effGraph.GetYaxis().SetTitle("Efficiency")
effGraph.GetYaxis().SetTitleSize(0.05)
effGraph.GetYaxis().SetTitleOffset(1.05)
effGraph.GetYaxis().SetLabelSize(0.03)
#c.SetRightMargin(0.18)
#c.SetLeftMargin(0.12)

title = TLatex()
title.SetTextSize(0.05);
#title.SetTextAlign(13);  
title.DrawLatexNDC(.2,.93,"CACTUS Pixel (5,3) Digital");
c.Update()
c.SaveAs("CACTUSEfficiencyVsX.gif")



##########################
#1D Efficiency Vs Y
##########################
den_Y = TH1F("den_Y",";X [mm];Number of Events",20,23,25)
num_Y = TH1F("num_Y",";X [mm];Number of Events",20,23,25)
tree.Draw("y_dut[2]>>den_Y","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0 && x_dut[2] > 19.52 && x_dut[2] < 20.45","colz")
tree.Draw("y_dut[2]>>num_Y","ntracks==1 && y_dut[0] > 0 && npix>0 && nback>0 && x_dut[2] > 19.52 && x_dut[2] < 20.45 && amp[3] > 200 ","colz")

nbins = num_Y.GetXaxis().GetNbins()
x = list()
y = list()
xErrLow = list()
xErrHigh = list()
yErrLow = list()
yErrHigh = list()

for b in range(1,nbins):

    xtemp = num_Y.GetXaxis().GetBinCenter(b+1)
    xerrlow =  num_Y.GetXaxis().GetBinCenter(b+1) - num_Y.GetXaxis().GetBinLowEdge(b+1)  
    xerrhigh = num_Y.GetXaxis().GetBinUpEdge(b+1) - num_Y.GetXaxis().GetBinCenter(b+1)  

    ratio = 0
    errLow = 0
    errHigh = 0

    n1 = int(num_Y.GetBinContent(b+1));
    n2 = int(den_Y.GetBinContent(b+1));
    print "numerator: " + str(n1) + " and denominator: " + str(n2)
    if (n1 > n2):
        n1 = n2;

    if (n2>0) :
      ratio = float(n1)/float(n2);
      if (ratio > 1) :
          ratio = 1;
      errLow = ratio - TEfficiency.ClopperPearson(n2, n1, 0.68269, False);
      errHigh = TEfficiency.ClopperPearson(n2, n1, 0.68269, True) - ratio;
    

    print " done bin " + str(b) + " " + str(xtemp) + " : " + str(n1) + "(" + str(num_Y.GetBinContent(b+1)) + ")" + " / " + str(n2) + "(" + str(den_Y.GetBinContent(b+1)) + ")" + " = " + str(ratio) + " " + str(errLow) + " " + str(errHigh)
    ytemp = ratio
    yerrlowtemp = errLow
    yerrhightemp = errHigh
    
    #if((yerrhightemp >= .5*ytemp) | (yerrlowtemp >= .5*ytemp)) continue; 
  
    print "x: " + str(xtemp) + " and y: " + str(ytemp)

    x.append(xtemp);  
    y.append(ytemp); 
    xErrLow.append(xerrlow);
    xErrHigh.append(xerrhigh);
    yErrLow.append(yerrlowtemp);
    yErrHigh.append(yerrhightemp);
    

xArr = array.array('f',x)
yArr = array.array('f',y)
xErrLowArr = array.array('f',xErrLow)
xErrHighArr = array.array('f',xErrHigh)
yErrLowArr = array.array('f',yErrLow)
yErrHighArr = array.array('f',yErrHigh)

effGraph = TGraphAsymmErrors(nbins, xArr, yArr, xErrLowArr, xErrHighArr, yErrLowArr,yErrHighArr );
effGraph.Draw("APE")
effGraph.SetTitle("")
effGraph.GetXaxis().SetTitle("Y [mm]")
effGraph.GetXaxis().SetTitleSize(0.05)
effGraph.GetXaxis().SetTitleOffset(0.90)
effGraph.GetXaxis().SetLabelSize(0.03)
effGraph.GetXaxis().SetRangeUser(23.0,25.0)
effGraph.GetYaxis().SetTitle("Efficiency")
effGraph.GetYaxis().SetTitleSize(0.05)
effGraph.GetYaxis().SetTitleOffset(1.05)
effGraph.GetYaxis().SetLabelSize(0.03)
#c.SetRightMargin(0.18)
#c.SetLeftMargin(0.12)

title = TLatex()
title.SetTextSize(0.05);
#title.SetTextAlign(13);  
title.DrawLatexNDC(.2,.93,"CACTUS Pixel (5,3) Digital");
c.Update()
c.SaveAs("CACTUSEfficiencyVsY.gif")

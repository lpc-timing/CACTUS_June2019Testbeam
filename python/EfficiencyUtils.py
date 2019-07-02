from ROOT import TFile,TTree,TCanvas,TH1F,TH2F,TLatex,TMath,TEfficiency,TGraphAsymmErrors
import array

##########################
#2D Efficiency 
##########################
def Plot2DEfficiency( num, den, plotname, topTitle, xAxisTitle, xAxisRangeLow, xAxisRangeHigh, yAxisTitle, yAxisRangeLow, yAxisRangeHigh, effMin, effMax ) :

    c = TCanvas("cv","cv",800,800)    

    ratio = num.Clone("ratio")
    ratio.Divide(den)

    ratio.Draw("colz")
    ratio.SetMaximum(effMax)
    ratio.SetMinimum(effMin)
    ratio.GetZaxis().SetTitle("Efficiency")
    ratio.GetZaxis().SetTitleSize(0.05)
    ratio.GetZaxis().SetTitleOffset(1.25)
    ratio.Draw("colz")
    ratio.SetStats(0)
    ratio.GetXaxis().SetTitle(xAxisTitle)
    ratio.GetXaxis().SetTitleSize(0.05)
    ratio.GetXaxis().SetTitleOffset(0.90)
    ratio.GetXaxis().SetLabelSize(0.03)
    ratio.GetXaxis().SetRangeUser(xAxisRangeLow,xAxisRangeHigh)
    ratio.GetYaxis().SetTitle(yAxisTitle)
    ratio.GetYaxis().SetTitleSize(0.05)
    ratio.GetYaxis().SetTitleOffset(1.05)
    ratio.GetYaxis().SetLabelSize(0.03)
    ratio.GetYaxis().SetRangeUser(yAxisRangeLow,yAxisRangeHigh)
    c.SetRightMargin(0.18)
    c.SetLeftMargin(0.12)

    title = TLatex()
    title.SetTextSize(0.05);
    #title.SetTextAlign(13);  
    title.DrawLatexNDC(.2,.93,topTitle);
    c.SaveAs(plotname+".gif")


##########################
#1D Efficiency 
##########################
def Plot1DEfficiency( num, den, plotname, topTitle, xAxisTitle, xAxisRangeLow, xAxisRangeHigh ) :

    nbins = num.GetXaxis().GetNbins()
    x = list()
    y = list()
    xErrLow = list()
    xErrHigh = list()
    yErrLow = list()
    yErrHigh = list()


    for b in range(1,nbins):

        xtemp = num.GetXaxis().GetBinCenter(b+1)
        xerrlow =  num.GetXaxis().GetBinCenter(b+1) - num.GetXaxis().GetBinLowEdge(b+1)  
        xerrhigh = num.GetXaxis().GetBinUpEdge(b+1) - num.GetXaxis().GetBinCenter(b+1)  

        ratio = 0
        errLow = 0
        errHigh = 0

        n1 = int(num.GetBinContent(b+1));
        n2 = int(den.GetBinContent(b+1));
        print "numerator: " + str(n1) + " and denominator: " + str(n2)
        if (n1 > n2):
            n1 = n2;

        if (n2>0) :
          ratio = float(n1)/float(n2);
          if (ratio > 1) :
              ratio = 1;
          errLow = ratio - TEfficiency.ClopperPearson(n2, n1, 0.68269, False);
          errHigh = TEfficiency.ClopperPearson(n2, n1, 0.68269, True) - ratio;
    

        print " done bin " + str(b) + " " + str(xtemp) + " : " + str(n1) + "(" + str(num.GetBinContent(b+1)) + ")" + " / " + str(n2) + "(" + str(den.GetBinContent(b+1)) + ")" + " = " + str(ratio) + " " + str(errLow) + " " + str(errHigh)
        ytemp = ratio
        yerrlowtemp = errLow
        yerrhightemp = errHigh
      
        print "x: " + str(xtemp) + " and y: " + str(ytemp)

        x.append(xtemp);  
        y.append(ytemp); 
        xErrLow.append(xerrlow);
        xErrHigh.append(xerrhigh);
        yErrLow.append(yerrlowtemp);
        yErrHigh.append(yerrhightemp);
    
    c = TCanvas("cv","cv",800,800)    
    c.SetLeftMargin(0.12)

    #must convert list into array for TGraphAsymmErrors to work
    xArr = array.array('f',x)
    yArr = array.array('f',y)
    xErrLowArr = array.array('f',xErrLow)
    xErrHighArr = array.array('f',xErrHigh)
    yErrLowArr = array.array('f',yErrLow)
    yErrHighArr = array.array('f',yErrHigh)

    effGraph = TGraphAsymmErrors(nbins, xArr, yArr, xErrLowArr, xErrHighArr, yErrLowArr,yErrHighArr );
    effGraph.Draw("APE")
    effGraph.SetTitle("")
    effGraph.GetXaxis().SetTitle(xAxisTitle)
    effGraph.GetXaxis().SetTitleSize(0.05)
    effGraph.GetXaxis().SetTitleOffset(0.90)
    effGraph.GetXaxis().SetLabelSize(0.03)
    effGraph.GetXaxis().SetRangeUser(xAxisRangeLow,xAxisRangeHigh)
    effGraph.GetYaxis().SetTitle("Efficiency")
    effGraph.GetYaxis().SetTitleSize(0.05)
    effGraph.GetYaxis().SetTitleOffset(1.05)
    effGraph.GetYaxis().SetLabelSize(0.03)

    title = TLatex()
    title.SetTextSize(0.05);
    title.DrawLatexNDC(.2,.93,topTitle);
    c.Update()
    c.SaveAs(plotname+".gif")

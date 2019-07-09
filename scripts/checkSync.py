from ROOT import TFile,TTree,TCanvas,TH2F
import os


StartRun = 16725
StopRun = 17039

InSyncRuns = list()
OutOfSyncRuns = list()

for Run in range(StartRun,StopRun+1,1):
    
    IsInSync = False
    inputfile = "/eos/uscms/store/user/cmstestbeam/2019_04_April_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v6/run_scope"+str(Run)+"_converted.root"

    if not os.path.exists(inputfile):
        print "input file "+inputfile+" does not exist"
        continue


    file = TFile(inputfile)
    tree = file.Get("pulse")
    c = TCanvas("cv","cv",800,800)

    num = TH2F("num",";x;y",25,0,50,25,0,50)
    den = TH2F("den",";x;y",25,0,50,25,0,50)
    tree.Draw("y_dut[0]:x_dut[0]>>den","ntracks==1 && y_dut[0] > 0 ","colz")
    tree.Draw("y_dut[0]:x_dut[0]>>num","ntracks==1 && y_dut[0] > 0 && amp[1] > 200 ","colz")

    num.Divide(den)

    effInside = num.GetBinContent(num.GetXaxis().FindFixBin(18.0),num.GetYaxis().FindFixBin(25.0))
    effOutside = num.GetBinContent(num.GetXaxis().FindFixBin(18.0),num.GetYaxis().FindFixBin(18.0))

    print num.GetXaxis().FindFixBin(18.0), " ", num.GetYaxis().FindFixBin(25.0), " ", effInside
    print num.GetXaxis().FindFixBin(18.0), " ", num.GetYaxis().FindFixBin(18.0), " ", effOutside


    if effInside > 0.80 and effOutside < 0.30:
        IsInSync = True

    print "Run "+str(Run)+" : "+str(IsInSync)

    if IsInSync:
        InSyncRuns.append(Run)
    else:
        OutOfSyncRuns.append(Run)



print "In Sync Runs"
print InSyncRuns
print "Out Of Sync Runs"
print OutOfSyncRuns


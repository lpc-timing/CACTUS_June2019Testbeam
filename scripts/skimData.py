from ROOT import TFile,TTree,TCanvas,TH2F
import os

########################
#Constants
########################


cutString_Pixel5_3 = "x_dut[2] > 19 && x_dut[2] < 21 && y_dut[2] > 23 && y_dut[2] < 25"
cutString_Pixel5_4 = "x_dut[2] > 18 && x_dut[2] < 20 && y_dut[2] > 23 && y_dut[2] < 25"
cutString_Pixel5_10 = "x_dut[2] > 19 && x_dut[2] < 21 && y_dut[2] > 22.5 && y_dut[2] < 24.5"

#Pixel5_3 : Run 16428
#Pixel5_4 : Run 17261
#Pixel5_10: Run 16725

runList_CACTUSDigital_HighThreshold = [16428, 16430, 16433, 16434, 16437, 16438, 16439, 16440, 16441, 16443, 16444, 16445, 16446, 16447, 16448, 16449, 16450, 16451, 16452, 16453, 16454]
runList_CACTUSDigital_LowThreshold = [16467, 16468, 16469, 16470, 16471, 16482, 16483, 16487, 16488]
runList_CACTUSDigital_TimingOptimized_HighThreshold = [16492, 16493, 16494, 16495, 16497, 16498, 16499, 16500, 16510, 16512, 16514]
runList_CACTUSAnalog_Pixel5_3_HighGain = [16719, 16720, 16721, 16722, 17040, 17042, 17043, 17044, 17045, 17046, 17047, 17048, 17049, 17050, 17051, 17052, 17053, 17054, 17055, 17057, 17058, 17059, 17060, 17061, 17062]
########################
#Skim Configuration
########################
cutString = cutString_Pixel5_3
runList = runList_CACTUSAnalog_Pixel5_3_HighGain

print "Run Skimming on runs:"
print runList
print "using cutString \"" + cutString + "\""
print "\n\n"


########################
#Start Skimming
########################

for Run in runList:
    print "Run "+str(Run)
    inputfileName = "/eos/uscms/store/user/cmstestbeam/2019_04_April_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v6/run_scope"+str(Run)+"_converted.root"
    outputfileName = "/eos/uscms/store/user/cmstestbeam/2019_04_April_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v6_CACTUSSkim/run_scope"+str(Run)+"_converted.root"

    if not os.path.exists(inputfileName):
        print "input file "+inputfileName+" does not exist"
        continue
 
    file = TFile(inputfileName)
    tree = file.Get("pulse")
    print "opened file "+inputfileName+" with "+str(tree.GetEntries())+" Events"

    outfile = TFile(outputfileName,"RECREATE")
    newTree = tree.CopyTree(cutString)    
    print "wrote output file"+outputfileName+" with "+str(newTree.GetEntries())+" Events"

    outfile.Write()
    outfile.Close()


    file.Close()

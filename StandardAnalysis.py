# coding: utf-8
import ROOT
import sys
from optparse import OptionParser
 
if __name__== '__main__':
  	# --------------------------------------------------------------------------------------------------------------------------------
	# Input 
	# --------------------------------------------------------------------------------------------------------------------------------
	#fileInput = ROOT.TFile('/afs/cern.ch/user/l/lbajan/CMSSW_7_4_15/src/CMSDIJET/DijetRootTreeAnalyzer/output/rootFile_reduced_skim.root')
        fileInput = ROOT.TFile.Open('root://eoscms.cern.ch//eos/cms/store/group/phys_exotica/dijet/Dijet13TeVScouting/rootTrees_reduced/ParkingScoutingMonitor-02-02-2016_20160202_191206/rootfile_ParkingScoutingMonitor_Run2015D-PromptReco-v4_JEC_HLT_v7_LowerCuts_20160304_reduced_skim.root')

        parser = OptionParser() 

        parser.add_option('--maxevents', type='int', action='store',
               default=-1,
               dest='maxevents',
               help='Number of events to run. -1 is all events')

        parser.add_option('--print_every', type='int', action='store',
               default=1000,
               dest='print_every',
               help='Print every nth event that is processed . -1 is all events')


        (options, args) = parser.parse_args()
        print options,args

	tree = fileInput.Get( 'rootTupleTree/tree' )
	nEntries = tree.GetEntriesFast()

	# Define histogram
        histo_mjj = ROOT.TH1F("mjj","",10000,0,10000)
        histo_mjj_btag0_loose = ROOT.TH1F("mjj_btag0_loose","",10000,0,10000)
        histo_mjj_btag1_loose = ROOT.TH1F("mjj_btag1_loose","",10000,0,10000)
        histo_mjj_btag2_loose = ROOT.TH1F("mjj_btag2_loose","",10000,0,10000)
        histo_mjj_btag0_medium = ROOT.TH1F("mjj_btag0_medium","",10000,0,10000)
        histo_mjj_btag1_medium = ROOT.TH1F("mjj_btag1_medium","",10000,0,10000)
        histo_mjj_btag2_medium = ROOT.TH1F("mjj_btag2_medium","",10000,0,10000)

	print 'Number of entries: ', nEntries

	# --------------------------------------------------------------------------------------------------------------------------------
	# Main loop
	# --------------------------------------------------------------------------------------------------------------------------------
        
        j=0 
        k=0 
        p=0
        loose=0.605
        medium=0.890
	for i in xrange(nEntries):

	        # Get event informations
	        tree.GetEntry(i)

                if options.maxevents > 0 and i > options.maxevents :
                   break              
  
                if i % options.print_every == 0 : 
                    print '---> Event ' + str(i)
                    print 'Selected events:', k 
                    print 'Run:', tree.run
             
                if not tree.passHLT_HT450 >0: 
                    continue 
                if not tree.PassJSON > 0  :
                    continue 
                if not tree.deltaETAjj < 1.3 :
                    continue
                if tree.mjj > 693 and tree.mjj < 838 :
                    continue
                #applie cuts on pT, eta, delta eta and mjj
#                if not tree.pTAK4_j1 > 60 :
#                   continue
#                if not tree.pTAK4_j2 > 30 :
#                   continue
#                if not abs(tree.etaAK4_j1) < 2.4 :
#                   continue
#                if not abs(tree.etaAK4_j2) < 2.4 :
#                   continue
                k+=1

                njetsl=0
                njetsm=0 
 
                if tree.jetCSVAK4_j1 > loose:
                    njetsl+=1
                if tree.jetCSVAK4_j2 > loose:
                    njetsl+=1

                if tree.jetCSVAK4_j1 > medium:
                     njetsm+=1
                if tree.jetCSVAK4_j2 > medium:
                     njetsm+=1

                
                if njetsl == 1:
                   histo_mjj_btag1_loose.Fill(tree.mjj)
                elif njetsl == 2:
                   histo_mjj_btag2_loose.Fill(tree.mjj)
                else:
                   histo_mjj_btag0_loose.Fill(tree.mjj)

                if njetsm == 1:
                   histo_mjj_btag1_medium.Fill(tree.mjj)
                elif njetsm == 2:
                   histo_mjj_btag2_medium.Fill(tree.mjj)
                else:
                   histo_mjj_btag0_medium.Fill(tree.mjj)
 
                histo_mjj.Fill(tree.mjj)


	# --------------------------------------------------------------------------------------------------------------------------------
	# Output, plots, ...
	# --------------------------------------------------------------------------------------------------------------------------------

	ROOT.gROOT.SetBatch(ROOT.kTRUE)
  



        #Create ROOT file
        outFile = ROOT.TFile('histo_mjj.root', 'recreate')
        histo_mjj.GetXaxis().SetTitle('mjj [GeV]')
        histo_mjj.Write()
        histo_mjj_btag0_loose.Write()
        histo_mjj_btag1_loose.Write()
        histo_mjj_btag2_loose.Write() 
        histo_mjj_btag0_medium.Write() 
        histo_mjj_btag1_medium.Write() 
        histo_mjj_btag2_medium.Write()

   

        outFile.Close()

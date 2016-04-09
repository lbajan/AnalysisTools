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
        pthisto = ROOT.TH2F("id0","",50,0,900,50,0,900)
        pthisto_j2 = ROOT.TH2F("id6","",50,0,900,50,0,900)
	histogram = ROOT.TH2F("id","",22,-0.05,1.05, 22,-0.05,1.05)
        histogram_j2 = ROOT.TH2F("id1","",22,-0.05,1.05, 22,-0.05,1.05)
        projection = ROOT.TH1D('id2', "1D Projection HLT JET 1", 22,-0.5,1.05)
        projection1 = ROOT.TH1D('id3', "1D Projection HLT JET 2", 22,-0.5,1.05)
        projectionX = ROOT.TH1D('id4', "1D Projection RECO JET 1", 22,-0.5,1.05)
        projectionX1 = ROOT.TH1D('id5', "1D Projection RECO JET 2", 22,-0.5,1.05)
        normalize =  ROOT.TH2F("id7","",22,-0.05,1.05, 22,-0.05,1.05)
        CSVHLTvspT1=ROOT.TH2F("id8","HLT CSV vs pT JET1",50,0,900,50,0,1.2)
        CSVRECOvspT1=ROOT.TH2F("id9","RECO CSV vs pT JET1",50,0,900,50,0,1.2)
        CSVHLTvspT2=ROOT.TH2F("eff_jet2","HLT CSV vs pT JET2",50,0,900,50,0,1.2)
        CSVRECOvspT2=ROOT.TH2F("eff_reco_jet2","RECO CSV vs pT JET2",50,0,900,50,0,1.2)

  
	print 'Number of entries: ', nEntries

	# --------------------------------------------------------------------------------------------------------------------------------
	# Main loop
	# --------------------------------------------------------------------------------------------------------------------------------
        
        j=0
	for i in xrange(nEntries):

	        # Get event informations
	        tree.GetEntry(i)

                if options.maxevents > 0 and i > options.maxevents :
                   break              
  
                if i % options.print_every == 0 : 
                    print '---> Event ' + str(i) 
#                if not tree.passHLT_CaloJet40 >0: 
#                    continue 
                if not tree.pTAK4_j1 > 60 :
                   continue
                if not tree.pTAK4_j2 > 30 :
                   continue
                if not tree.pTAK4_recoj1 > 60 :
                   continue
                if not tree.pTAK4_recoj2 > 30 :
                   continue
                if not abs(tree.etaAK4_j1) < 2.5 :
                   continue
                if not abs(tree.etaAK4_j2) < 2.5 :
                   continue
                if not abs(tree.etaAK4_recoj1) < 2.5 :
                   continue
                if not abs(tree.etaAK4_recoj2) < 2.5 :
                   continue
#                if not tree.deltaETAjj < 1.3 :
#                   break
#                if tree.deltaETAjjreco > 1.3 : #treba li za reco?
#                   break
#                if tree.mjj < 500 :
#                   break
#                if tree.mjjreco < 500 :
#                   break



                #HLT jets
                jets=[]   #empty list for HLT jets
                jet1=ROOT.TLorentzVector() #initialize Lorentz vector components for HLT jet1
                jet2=ROOT.TLorentzVector() #initialize Lorentz vector components for HLT jet2
                jet1.SetPtEtaPhiM(tree.pTAK4_j1,tree.etaAK4_j1,tree.phiAK4_j1,tree.massAK4_j1) #set values with variables from tree   
                jet2.SetPtEtaPhiM(tree.pTAK4_j2,tree.etaAK4_j2,tree.phiAK4_j2,tree.massAK4_j2) #set values with variables from tree
                jets.append(jet1) #append HLT jet1 to list jets
                jets.append(jet2) #append HLT jet2 to list jets
                CSV=[tree.jetCSVAK4_j1,tree.jetCSVAK4_j2] #create list with CSV for each jet

                #RECO jets
                jets_Reco=[] #empty list for RECO jets
                jet1_Reco=ROOT.TLorentzVector() #initialize Lorentz vector components for RECO jet1
                jet2_Reco=ROOT.TLorentzVector() #initialize Lorentz vector components for RECO jet2
                jet1_Reco.SetPtEtaPhiM(tree.pTAK4_recoj1,tree.etaAK4_recoj1,tree.phiAK4_recoj1,tree.massAK4_recoj1) #set values
                jet2_Reco.SetPtEtaPhiM(tree.pTAK4_recoj2,tree.etaAK4_recoj2,tree.phiAK4_recoj2,tree.massAK4_recoj2) #set values
	        jets_Reco.append(jet1_Reco) #append RECO jet1 to list jets 
                jets_Reco.append(jet2_Reco) #append RECO jet2 to list jets
                CSV_reco=[tree.jetCSVAK4_recoj1,tree.jetCSVAK4_recoj2] #create list with CSV for each jet                

                #distance between HLT and RECO jets
                DeltaReco1HLT1=jets_Reco[0].DeltaR(jets[0])
                DeltaReco1HLT2=jets_Reco[1].DeltaR(jets[1])
                DeltaReco2HLT1=jets_Reco[1].DeltaR(jets[0])
                DeltaReco2HLT2=jets_Reco[1].DeltaR(jets[1])

                #IdxMatching list
                IdxMatching=[]
                #if..elif..else statement determins which RECO jet is closer to HLT1 jet
                #and sets condition on distance 
                if DeltaReco1HLT1 <= DeltaReco2HLT1 and DeltaReco1HLT1 < 0.2:
                   IdxMatching.append(0)
                   IdxMatching.append(1)
                elif DeltaReco2HLT1 < DeltaReco1HLT1 and DeltaReco2HLT1 < 0.2:
                   IdxMatching.append(1)
                   IdxMatching.append(0)
                else:
                   IdxMatching.append(-1) #distance between RECO and scouting jet is greater than 0.2
                if not IdxMatching[0] < 0:
                       CSV_temp = (-0.025 if CSV[0]<0 else CSV[0]) #remapping of negative CSV values for HLT
                       CSV_temp_reco = (-0.025 if CSV_reco[IdxMatching[0]]<0 else CSV_reco[IdxMatching[0]]) #remapping for RECO
                       CSV_temp_j2 = (-0.025 if CSV[1]<0 else CSV[1])
                       CSV_temp_reco_j2 = (-0.025 if CSV_reco[IdxMatching[1]]<0 else CSV_reco[IdxMatching[1]])
                       histogram.Fill(CSV_temp,CSV_temp_reco)
                       histogram_j2.Fill(CSV_temp_j2,CSV_temp_reco_j2)
   
      
                else:
                       j+=1
                pthisto.Fill(tree.pTAK4_j1,tree.pTAK4_recoj1) #histogram for determinig correlation factor for 1st leading jet
                pthisto_j2.Fill(tree.pTAK4_j2,tree.pTAK4_recoj2) #histogram for determining correlation factor for 2nd leading jet
                CSVHLTvspT1.Fill(tree.pTAK4_j1,tree.jetCSVAK4_j1)
                CSVRECOvspT1.Fill(tree.pTAK4_j1,tree.jetCSVAK4_recoj1)
                CSVHLTvspT2.Fill(tree.pTAK4_j2,tree.jetCSVAK4_j2)
                CSVRECOvspT2.Fill(tree.pTAK4_j2,tree.jetCSVAK4_recoj2)

              
               
        print "IdxMatching[0] is negative %d times. " %j 
        print "Correlation factor for HLT CSV and RECO CSV for 1st leading jet is:", histogram.GetCorrelationFactor() 
        print "Correlation factor for HLT CSV and RECO CSV for 2nd leading jet is:", histogram_j2.GetCorrelationFactor()
        print "Correlation factor for pT RECO and HLT for 1st leading jet is:", pthisto.GetCorrelationFactor() 
        print "Correlation factor for pT RECO and HLT for 2nd leading jet is:", pthisto_j2.GetCorrelationFactor()
        projection=histogram.ProjectionY()
        projection1=histogram_j2.ProjectionY()
        projectionX=histogram.ProjectionX()
        projectionX1=histogram_j2.ProjectionX()


        #Normalize the 2D HLT vs RECO CSV plot 
        nxbins=histogram.GetNbinsX()
        nybins=histogram.GetNbinsY()
        i=1
        while i <= nxbins:
            j=1
            N=histogram.ProjectionY('y',i,i).Integral(0,nybins+1)
            #print N
            while j<=nybins:
               if N > 0:
                  normalize.SetBinContent(i,j,histogram.GetBinContent(i,j)/N) 
               j+=1
            i+=1
        
#        nxbins=histogram.GetNbinsX() 
#        nybins=histogram.GetNbinsY()
#        i=0
#        while i <= nxbins:
#              htemp=histogram.ProjectionY('y',i,i)
#              htemp.GetXaxis().SetTitle('RECO CSV')
#              htemp.GetYaxis().SetTitle('ENTRIES')
#              htemp.SetFillColor(50)
#              htemp.SetStats(0) 
#              htemp.SaveAs('Projection_'+str(i)+'.root')
#              i+=1

	# --------------------------------------------------------------------------------------------------------------------------------
	# Output, plots, ...
	# --------------------------------------------------------------------------------------------------------------------------------

	ROOT.gROOT.SetBatch(ROOT.kTRUE)
  
        nxbins=histogram.GetNbinsX() 
        nybins=histogram.GetNbinsY()
        i=0
        while i <= nxbins:
              htemp=normalize.ProjectionY('y',i,i)
              e = ROOT.TCanvas( 'test', 'test', 1200, 1000)
	      e.cd()
              #histogram.Draw('LEGO2Z')
              htemp.Draw('colz') # "colz"
	      #histogram.SetTitle(namesTF[i])
	      htemp.GetXaxis().SetTitle('RECO CSV')
              htemp.GetYaxis().SetTitle('ENTRIES')			
	      #h[i].GetYaxis().SetTitle("SCEta");
              #histogram.GetColorTransparent(55, 0.3)
              #ROOT.gStyle.SetPalette(107)
              htemp.SetFillColor(50)
              ROOT.gStyle.SetOptStat(0)
              #ROOT.gStyle.SetOptStat("nemruoi")
              e.SetLogz()
	      e.SaveAs('Projection_'+ str(i) +'.pdf')
              i+=1


        #plot for 1st leading scouting jet
	c = ROOT.TCanvas( 'test', 'test', 1200, 1000)
	c.cd()
        #histogram.Draw('LEGO2Z')
        histogram.Draw('colz') # "colz"
	#histogram.SetTitle(namesTF[i])
	histogram.GetXaxis().SetTitle('HLT CSV')
        histogram.GetYaxis().SetTitle('RECO CSV')			
	#h[i].GetYaxis().SetTitle("SCEta");
        #histogram.GetColorTransparent(55, 0.3)
        #ROOT.gStyle.SetPalette(107)
        ROOT.gStyle.SetOptStat(0)
        #ROOT.gStyle.SetOptStat("nemruoi")
        c.SetLogz()
	c.SaveAs('matching.pdf')
 
 
        #plot for 2nd leading scouting jet
        h = ROOT.TCanvas( 'test', 'test', 1200, 1000)
        h.cd()
        #histogram.Draw('LEGO2Z')
        histogram_j2.Draw('colz') # "colz"
        #histogram.SetTitle(namesTF[i])
        histogram_j2.GetXaxis().SetTitle('HLT CSV')
        histogram_j2.GetYaxis().SetTitle('RECO CSV')                       
        #h[i].GetYaxis().SetTitle("SCEta");
        #ROOT.gStyle.SetPalette(29)
        ROOT.gStyle.SetOptStat(0)
        #ROOT.gStyle.SetOptStat("nemruoi")
        h.SetLogz()
        h.SaveAs('matching_j2.pdf')

        #plot 1D projection on the Y axis for 1st leading scouting jet
        k = ROOT.TCanvas( 'test', 'test', 1200, 1000)
        k.cd()
        #histogram.Draw('LEGO2Z')
        projection.Draw() # "colz"
        projection.SetTitle('1D PROJECTION ON THE Y AXIS JET1')
        projection.GetXaxis().SetTitle('RECO CSV')
        projection.GetYaxis().SetTitle('Entries')
        #h[i].GetYaxis().SetTitle("SCEta");
        #ROOT.gStyle.SetPalette(29)
        ROOT.gStyle.SetOptStat(0)
        projection.SetFillColor(9)
        #ROOT.gStyle.SetOptStat("nemruoi")
        #k.SetLogz()
        k.SaveAs('projection.pdf')
        
        #plot 1D projection on the Y axis for 2nd leading scouting jet
        l = ROOT.TCanvas( 'test', 'test', 1200, 1000)
        l.cd()
        #histogram.Draw('LEGO2Z')
        projection1.Draw() # "colz"
        projection1.SetTitle('1D PROJECTION ON THE Y AXIS JET2')
        projection1.GetXaxis().SetTitle('RECO CSV')
        projection1.GetYaxis().SetTitle('Entries')
        #h[i].GetYaxis().SetTitle("SCEta");
        #ROOT.gStyle.SetPalette(29)
        ROOT.gStyle.SetOptStat(0)
        projection1.SetFillColor(8)
        #ROOT.gStyle.SetOptStat("nemruoi")
        #k.SetLogz()
        l.SaveAs('projection_j2.pdf')
  
        #plot 1D projection on the X axis for the 1st leading reco jet 
        m = ROOT.TCanvas( 'test', 'test', 1200, 1000)
        m.cd()
        #histogram.Draw('LEGO2Z')
        projectionX.Draw() # "colz"
        projectionX.SetTitle('1D PROJECTION ON THE X AXIS JET1')
        projectionX.GetXaxis().SetTitle('HLT CSV')
        projectionX.GetYaxis().SetTitle('Entries')
        #h[i].GetYaxis().SetTitle("SCEta");
        #ROOT.gStyle.SetPalette(29)
        ROOT.gStyle.SetOptStat(0)
        projectionX.SetFillColor(6)
        #ROOT.gStyle.SetOptStat("nemruoi")
        #k.SetLogz()
        m.SaveAs('projectionX.pdf')

        #plot 1D projection on the X axis for the 2st leading reco jet 
        n = ROOT.TCanvas( 'test', 'test', 1200, 1000)
        n.cd()
        #histogram.Draw('LEGO2Z')
        projectionX1.Draw() # "colz"
        projectionX1.SetTitle('1D PROJECTION ON THE X AXIS JET2')
        projectionX1.GetXaxis().SetTitle('HLT CSV')
        projectionX1.GetYaxis().SetTitle('Entries')
        #h[i].GetYaxis().SetTitle("SCEta");
        #ROOT.gStyle.SetPalette(29)
        ROOT.gStyle.SetOptStat(0)
        projectionX1.SetFillColor(40)
        #ROOT.gStyle.SetOptStat("nemruoi")
        #k.SetLogz()
        n.SaveAs('projectionX1.pdf')

        #plot 1D projection on the X axis for the 2st leading reco jet 
        p = ROOT.TCanvas( 'test', 'test', 1300, 1050)
        p.cd()
        #histogram.Draw('LEGO2Z')
        pthisto.Draw() # "colz"
        #pthisto.SetTitle('pTAK4 RECO VS HLT FOR LEADING JET')
        pthisto.GetXaxis().SetTitle('HLT pT')
        pthisto.GetYaxis().SetTitle('RECO pT')
        #h[i].GetYaxis().SetTitle("SCEta");
        #ROOT.gStyle.SetPalette(29)
        ROOT.gStyle.SetOptStat(0)
        #projectionX1.SetFillColor(40)
        #ROOT.gStyle.SetOptStat("nemruoi")
        #k.SetLogz()
        p.SaveAs('ptRECO_VS_HLT.pdf')

        #plot 1D projection on the X axis for the 2st leading reco jet 
        p1 = ROOT.TCanvas( 'test', 'test', 1300, 1050)
        p1.cd()
        #histogram.Draw('LEGO2Z')
        pthisto_j2.Draw() # "colz"
        #pthisto_j2.SetTitle('pTAK4 RECO VS HLT FOR LEADING JET')
        pthisto_j2.GetXaxis().SetTitle('HLT pT')
        pthisto_j2.GetYaxis().SetTitle('RECO pT')
        #h[i].GetYaxis().SetTitle("SCEta");
        #ROOT.gStyle.SetPalette(29)
        ROOT.gStyle.SetOptStat(0)
        #projectionX1.SetFillColor(40)
        #ROOT.gStyle.SetOptStat("nemruoi")
        #k.SetLogz()
        p1.SaveAs('ptRECO_VS_HLT_j2.pdf')


        #Normalization of HLT vs RECO CSV plot 
        s = ROOT.TCanvas( 'test', 'test', 1200, 1000)
#        ROOT.gStyle.SetCanvasDefH(1500)
#        ROOT.gStyle.SetCanvasDefW(1500)
        s.cd()
        s.SetRightMargin(0.13)
        #histogram.Draw('LEGO2Z')
        normalize.Draw('colztext') # "colz"
        #normalize.SetTitle('NORMALIZED HLT VS RECO CSV PLOT')
        normalize.GetXaxis().SetTitle('HLT CSV')
        normalize.GetYaxis().SetTitle('RECO CSV')
        #h[i].GetYaxis().SetTitle("SCEta");
        #ROOT.gStyle.SetPalette(29)
        ROOT.gStyle.SetPaintTextFormat("4.2f")
        ROOT.gStyle.SetOptStat(0)
        #projectionX1.SetFillColor(40)
        #ROOT.gStyle.SetOptStat("nemruoi")
        s.SetLogz()
        s.SaveAs('normalization.pdf')


	#Create ROOT file
	outFile =ROOT.TFile('CSV_HLT_vs_pT_jet1.root', 'recreate')
        #outFile.cd()
        CSVHLTvspT1.Write()
        outFile.Close()

        #Create ROOT file
        outFile = ROOT.TFile('CSV_RECO_vs_pT_jet1.root', 'recreate')
        #outFile.cd()
        CSVRECOvspT1.Write()
        outFile.Close()

        #Create ROOT file
	outFile =ROOT.TFile('CSV_HLT_vs_pT_jet2.root', 'recreate')
        #outFile.cd()
        CSVHLTvspT2.Write()
        outFile.Close()

        #Create ROOT file
        outFile = ROOT.TFile('CSV_RECO_vs_pT_jet2.root', 'recreate')
        outFile.cd()
        CSVRECOvspT2.Write()
        outFile.Close()
  
        #Create ROOT file
        outFile = ROOT.TFile('matching.root', 'recreate')
        outFile.cd()
        histogram.Write()
        outFile.Close()

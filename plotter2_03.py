###This file is for plotting.

import ROOT as r
from   ROOT import gROOT, TCanvas, TFile, TGraphErrors, SetOwnership, TVector3
###
from ROOT import TLorentzVector
###
import math, sys, optparse, array, copy, os
import gc, inspect
import numpy as np

#import include.Sample as Sample
#import include.helper as helper
#import include.Canvas as Canvas
#import include.Efficiency as Efficiency

import errno

'''
### Combining plots for a single signal a time ## 


###Read ROOT file to plot
f = r.TFile("SimpleExample_test_1000_150_100/Output.root")

###Define canvas
c1 = r.TCanvas("c1", "Transverse momentum pt")
c2 = r.TCanvas("c2", "Psudorapidity")
c3 = r.TCanvas("c3", "Energy")

### Combined plots
    
### C1
f.h_ptEl.SetLineColor(r.kRed)
f.h_ptEl.SetLineWidth(2)
f.h_ptMu.SetLineColor(r.kBlue)
f.h_ptMu.SetLineWidth(2)
f.h_ptX.SetLineColor(r.kOrange)
f.h_ptX.SetLineWidth(2)
f.h_ptH.SetLineColor(r.kGreen)
f.h_ptH.SetLineWidth(2)
    
f.h_ptEl.SetTitle("Transverse Momentum pt") # The title is the one from first histogram, so it is changed accordingly.
#r.gStyle.SetOptTitle(r.kFALSE)
r.gStyle.SetOptStat(0)

c1.cd()
f.h_ptEl.Draw("SAME")
f.h_ptMu.Draw("SAME")
f.h_ptX.Draw("SAME")
f.h_ptH.Draw("SAME")
    
#c1.SetTitle("c1")
    
legendc1 = r.TLegend()
legendc1.SetTextSize(0.02)
legendc1.SetBorderSize(1)
legendc1.AddEntry("h_ptEl","pt electron","l")
legendc1.AddEntry("h_ptMu","pt muon","l")
legendc1.AddEntry("h_ptX","pt X boson","l")
legendc1.AddEntry("h_ptH","pt Higgs boson","l")
legendc1.Draw('SAME')

### C2
f.h_etaEl.SetLineColor(r.kRed)
f.h_etaEl.SetLineWidth(2)
f.h_etaMu.SetLineColor(r.kBlue)
f.h_etaMu.SetLineWidth(2)
f.h_etaX.SetLineColor(r.kOrange)
f.h_etaX.SetLineWidth(2)
    
f.h_etaEl.SetTitle("Pseudorapidity") # The title is the one from first histogram, so it is changed accordingly.
#r.gStyle.SetOptTitle(r.kFALSE)
#r.gStyle.SetOptStat(0)

c2.cd()
f.h_etaEl.Draw("SAME")
f.h_etaMu.Draw("SAME")
f.h_etaX.Draw("SAME")
    
#c1.SetTitle("c1")
    
legendc2 = r.TLegend()
legendc2.SetTextSize(0.02)
legendc2.SetBorderSize(1)
legendc2.AddEntry("h_etaEl","eta electron","l")
legendc2.AddEntry("h_etaMu","eta muon","l")
legendc2.AddEntry("h_etaX","eta X boson","l")
legendc2.Draw('SAME')

### C3
f.h_EEl.SetLineColor(r.kRed)
f.h_EEl.SetLineWidth(2)
f.h_EMu.SetLineColor(r.kBlue)
f.h_EMu.SetLineWidth(2)
f.h_EX.SetLineColor(r.kOrange)
f.h_EX.SetLineWidth(2)
f.h_EH.SetLineColor(r.kGreen)
f.h_EH.SetLineWidth(2)
    
f.h_EX.SetTitle("Energy") # The title is the one from first histogram, so it is changed accordingly.
#r.gStyle.SetOptTitle(r.kFALSE)
#r.gStyle.SetOptStat(0)

c3.cd()
f.h_EX.Draw("SAME")
f.h_EMu.Draw("SAME")
f.h_EEl.Draw("SAME")
f.h_EH.Draw("SAME")
    
#c1.SetTitle("c1")
    
legendc3 = r.TLegend()
legendc3.SetTextSize(0.02)
legendc3.SetBorderSize(1)
legendc3.AddEntry("h_EEl","E electron","l")
legendc3.AddEntry("h_EMu","E muon","l")
legendc3.AddEntry("h_EX","E X boson","l")
legendc3.AddEntry("h_EH","E Higgs boson","l")
legendc3.Draw('SAME')

### Write
c1.Print("SimpleExample_test_1000_150_100/c1.pdf")
c2.Print("SimpleExample_test_1000_150_100/c2.pdf")
c3.Print("SimpleExample_test_1000_150_100/c3.pdf")


f.Close()
'''

###
### Combining plots for different signals ##
try:
    os.mkdir("Combined")
except OSError as exc:
    if exc.errno != errno.EEXIST:
        raise
    pass

f1 = r.TFile("SimpleExample_test_1000_150_100/Output.root")
f2 = r.TFile("SimpleExample_test_1000_350_350/Output.root")
f3 = r.TFile("SimpleExample_test_400_150_400/Output.root")
f4 = r.TFile("SimpleExample_test_400_50_40/Output.root")

f5 = r.TFile("SimpleExample_test_400_50_400/Output.root")
f6 = r.TFile("SimpleExample_test_400_50_4/Output.root")
f7 = r.TFile("SimpleExample_test_1000_150_10/Output.root")
f8 = r.TFile("SimpleExample_test_1000_350_35/Output.root")

### Check the flag for lepton selection
flgck = f1.flagcheck.GetEntries()
if (flgck == 0):
  leptselec = "GenLeptonSel"
else:
  leptselec = "HardProcessParticle"
###

canvas = r.TCanvas("Combined_histo", "Combined_histo")
canvas.Print("Combined/All_histograms_{}.pdf[".format(leptselec))
canvas.Print("Combined/All_histograms_Logy_{}.pdf[".format(leptselec))

### Text choices for Legends
Ltxt0 = ["1000_150_100", "1000_350_350", "400_150_400", "400_50_40"]
Ltxt1 = ["400_50_400", "400_150_400", "400_50_4", "400_50_40"]
Ltxt2 = ["1000_150_100", "1000_150_10", "1000_350_350", "1000_350_35"]
###


### Function for generating plots
def PlotCombined(histo1, histo2, histo3, histo4, shortname, longname, legendtext, xlabel, ylabel):
  canvas.Clear()
  
  histo1.SetName("h_1")
  histo2.SetName("h_2")
  histo3.SetName("h_3")
  histo4.SetName("h_4")

  histo1.SetLineColor(r.kRed)
  histo1.SetLineWidth(2)
  histo2.SetLineColor(r.kBlue)
  histo2.SetLineWidth(2)
  histo3.SetLineColor(r.kOrange-3)
  histo3.SetLineWidth(2)
  histo4.SetLineColor(r.kGreen+1)
  histo4.SetLineWidth(2)

  stack = r.THStack("hs","{0}; {1}; {2}".format(longname, xlabel, ylabel))
  stack.Add(histo1)
  stack.Add(histo2)
  stack.Add(histo3)
  stack.Add(histo4)
  
  canvas.SetLogy(0)	# Force it to not use Log scale
  stack.Draw("nostack")
        
  legend_canvas = r.TLegend(0.75, 0.7, 0.9, 0.9, "Signal")
  legend_canvas.SetTextSize(0.02)
  #legend_canvas.SetBorderSize(1)
  legend_canvas.AddEntry("h_1","{}".format(legendtext[0]),"l")
  legend_canvas.AddEntry("h_2","{}".format(legendtext[1]),"l")
  legend_canvas.AddEntry("h_3","{}".format(legendtext[2]),"l")
  legend_canvas.AddEntry("h_4","{}".format(legendtext[3]),"l")
  legend_canvas.Draw("SAME")
 
  canvas.Print("Combined/c_{}.pdf".format(shortname))
  canvas.Print("Combined/c_{}.png".format(shortname))
  canvas.Print("Combined/All_histograms_{}.pdf".format(leptselec))
  
  ### Plots with log scale in y axis
  canvas.Clear()
  canvas.SetLogy(1)	# Use Log scale
  stack.Draw("nostack")
  legend_canvas = r.TLegend(0.75, 0.7, 0.9, 0.9, "Signal")
  legend_canvas.SetTextSize(0.02)
  #legend_canvas.SetBorderSize(1)
  legend_canvas.AddEntry("h_1","{}".format(legendtext[0]),"l")
  legend_canvas.AddEntry("h_2","{}".format(legendtext[1]),"l")
  legend_canvas.AddEntry("h_3","{}".format(legendtext[2]),"l")
  legend_canvas.AddEntry("h_4","{}".format(legendtext[3]),"l")
  legend_canvas.Draw("SAME")
  canvas.Print("Combined/c_{}_Logy.pdf".format(shortname))
  canvas.Print("Combined/c_{}_Logy.png".format(shortname))
  canvas.Print("Combined/All_histograms_Logy_{}.pdf".format(leptselec))
  
def TwoDHistogramsDivided4(histo1, histo2, histo3, histo4, shortname, longname, legendtext, xlabel, ylabel):
  canvas.Clear()
  canvas.SetLogy(0)	# Force it to not use Log scale in y
  canvas.SetLogz(1)	# Use Log scale in z
  canvas.Divide(2, 2, 0.02, 0.02)
  
  histo1.SetTitle("{0} {1}".format(longname, legendtext[0]))
  histo2.SetTitle("{0} {1}".format(longname, legendtext[1]))
  histo3.SetTitle("{0} {1}".format(longname, legendtext[2]))
  histo4.SetTitle("{0} {1}".format(longname, legendtext[3]))
  
  histo1.GetXaxis().SetTitle(xlabel)
  histo1.GetYaxis().SetTitle(ylabel)
  histo1.SetStats(0)
  histo2.GetXaxis().SetTitle(xlabel)
  histo2.GetYaxis().SetTitle(ylabel)
  histo2.SetStats(0)
  histo3.GetXaxis().SetTitle(xlabel)
  histo3.GetYaxis().SetTitle(ylabel)
  histo3.SetStats(0)
  histo4.GetXaxis().SetTitle(xlabel)
  histo4.GetYaxis().SetTitle(ylabel)
  histo4.SetStats(0)
  
  canvas.cd(1)
  canvas.cd(1).SetLogz(1)
  histo1.Draw("colz")  
  canvas.cd(2)
  canvas.cd(2).SetLogz(1)
  histo2.Draw("colz")  
  canvas.cd(3)
  canvas.cd(3).SetLogz(1)
  histo3.Draw("colz")
  canvas.cd(4)
  canvas.cd(4).SetLogz(1)
  histo4.Draw("colz")
  
  canvas.Print("Combined/2D_{}.pdf".format(shortname))
  canvas.Print("Combined/2D_{}.png".format(shortname))
  canvas.Print("Combined/All_histograms_{}.pdf".format(leptselec))
  


### Ask for the desired plots
'''
PlotCombined(f1.h_ptMu, f2.h_ptMu, f3.h_ptMu, f4.h_ptMu, "ptMu", "Muon transverse momentum p_{T}", Ltxt0, "p_{T} (GeV)", "Events")
PlotCombined(f1.h_ptEl, f2.h_ptEl, f3.h_ptEl, f4.h_ptEl, "ptEl", "Electron transverse momentum p_{T}", Ltxt0, "p_{T} (GeV)", "Events")
PlotCombined(f1.h_ptX, f2.h_ptX, f3.h_ptX, f4.h_ptX, "ptX", "X boson transverse momentum p_{T}", Ltxt0, "p_{T} (GeV)", "Events")
PlotCombined(f1.h_ptH, f2.h_ptH, f3.h_ptH, f4.h_ptH, "ptH", "H boson transverse momentum p_{T}", Ltxt0, "p_{T} (GeV)", "Events")

PlotCombined(f1.h_EMu, f2.h_EMu, f3.h_EMu, f4.h_EMu, "EMu", "Muon energy", Ltxt0, "E", "Events")
PlotCombined(f1.h_EEl, f2.h_EEl, f3.h_EEl, f4.h_EEl, "EEl", "Electron energy", Ltxt0, "E", "Events")
PlotCombined(f1.h_EX, f2.h_EX, f3.h_EX, f4.h_EX, "EX", "X boson energy", Ltxt0, "E", "Events")
PlotCombined(f1.h_EH, f2.h_EH, f3.h_EH, f4.h_EH, "EH", "Higgs boson energy", Ltxt0, "E", "Events")

PlotCombined(f1.h_etaMu, f2.h_etaMu, f3.h_etaMu, f4.h_etaMu, "etaMu", "Muon Pseudorapidity", Ltxt0, "#eta", "Events")
PlotCombined(f1.h_etaEl, f2.h_etaEl, f3.h_etaEl, f4.h_etaEl, "etaEl", "Electron Pseudorapidity", Ltxt0, "#eta", "Events")
PlotCombined(f1.h_etaX, f2.h_etaX, f3.h_etaX, f4.h_etaX, "etaX", "X boson Pseudorapidity", Ltxt0, "#eta", "Events")

PlotCombined(f1.h_gammaX, f2.h_gammaX, f3.h_gammaX, f4.h_gammaX, "gammaX", "X boson Lorentz factor", Ltxt0, "#gamma", "Events" )

PlotCombined(f1.h_mumuAngle_XXmumuee, f2.h_mumuAngle_XXmumuee, f3.h_mumuAngle_XXmumuee, f4.h_mumuAngle_XXmumuee, "mumuAngle_XXmumuee", "Angle between muons for final state with mu, mu, e, e", Ltxt0, "#alpha (rad)", "Events")
PlotCombined(f1.h_eeAngle_XXmumuee, f2.h_eeAngle_XXmumuee, f3.h_eeAngle_XXmumuee, f4.h_eeAngle_XXmumuee, "eeAngle_XXmumuee", "Angle between electrons for final state with mu, mu, e, e", Ltxt0, "#alpha (rad)", "Events")
PlotCombined(f1.h_mumuAngle_XXmumumumu, f2.h_mumuAngle_XXmumumumu, f3.h_mumuAngle_XXmumumumu, f4.h_mumuAngle_XXmumumumu, "mumuAngle_XXmumumumu", "Angle between muons for final state with mu, mu, mu, mu", Ltxt0, "#alpha (rad)", "Events")
PlotCombined(f1.h_eeAngle_XXeeee , f2.h_eeAngle_XXeeee , f3.h_eeAngle_XXeeee, f4.h_eeAngle_XXeeee , "eeAngle_XXeeee ", "Angle between electrons for final state with e, e, e, e", Ltxt0, "#alpha (rad)", "Events")

PlotCombined(f1.h_LX_Mu, f2.h_LX_Mu, f3.h_LX_Mu, f4.h_LX_Mu, "LX_Mu", "X boson traveled distance before producing muon", Ltxt0, "L", "Events")
PlotCombined(f1.h_LxyX_Mu, f2.h_LxyX_Mu, f3.h_LxyX_Mu, f4.h_LxyX_Mu, "LxyX_Mu", "X boson traveled distance in xy plane before producing muon", Ltxt0, "L_{xy}", "Events")
PlotCombined(f1.h_LX_El, f2.h_LX_El, f3.h_LX_El, f4.h_LX_El, "LX_El", "X boson traveled distance before producing electron", Ltxt0, "L", "Events")
PlotCombined(f1.h_LxyX_El, f2.h_LxyX_El, f3.h_LxyX_El, f4.h_LxyX_El, "LxyX_El", "X boson traveled distance in xy plane before producing electron", Ltxt0, "L_{xy}", "Events")

PlotCombined(f1.h_LX_Mu_Xframe, f2.h_LX_Mu_Xframe, f3.h_LX_Mu_Xframe, f4.h_LX_Mu_Xframe, "LX_Mu_Xframe", "X boson traveled distance before producing muon. Frame with X at rest.", Ltxt0, "L", "Events")
PlotCombined(f1.h_LxyX_Mu_Xframe, f2.h_LxyX_Mu_Xframe, f3.h_LxyX_Mu_Xframe, f4.h_LxyX_Mu_Xframe, "LxyX_Mu_Xframe", "X boson traveled distance in xy plane before producing muon. Frame with X at rest.", Ltxt0, "L_{xy}", "Events")
PlotCombined(f1.h_LX_El_Xframe, f2.h_LX_El_Xframe, f3.h_LX_El_Xframe, f4.h_LX_El_Xframe, "LX_El_Xframe", "X boson traveled distance before producing electron. Frame with X at rest.", Ltxt0, "L", "Events")
PlotCombined(f1.h_LxyX_El_Xframe, f2.h_LxyX_El_Xframe, f3.h_LxyX_El_Xframe, f4.h_LxyX_El_Xframe, "LxyX_El", "X boson traveled distance in xy plane before producing electron. Frame with X at rest.", Ltxt0, "L_{xy}", "Events")

### L and Lxy for same kinematics 1
PlotCombined(f5.h_LX_Mu, f3.h_LX_Mu, f6.h_LX_Mu, f4.h_LX_Mu, "LX_Mu_samekin1", "X boson traveled distance before producing muon. Same kinematics 1.", Ltxt1, "L", "Events")
PlotCombined(f5.h_LxyX_Mu, f3.h_LxyX_Mu, f6.h_LxyX_Mu, f4.h_LxyX_Mu, "LxyX_Mu_samekin1", "X boson traveled distance in xy plane before producing muon. Same kinematics 1.", Ltxt1, "L_{xy}", "Events")
PlotCombined(f5.h_LX_El, f3.h_LX_El, f6.h_LX_El, f4.h_LX_El, "LX_El_samekin1", "X boson traveled distance before producing electron. Same kinematics 1.", Ltxt1, "L", "Events")
PlotCombined(f5.h_LxyX_El, f3.h_LxyX_El, f6.h_LxyX_El, f4.h_LxyX_El, "LxyX_El_samekin1", "X boson traveled distance in xy plane before producing electron. Same kinematics 1.", Ltxt1, "L_{xy}", "Events")

PlotCombined(f5.h_LX_Mu_Xframe, f3.h_LX_Mu_Xframe, f6.h_LX_Mu_Xframe, f4.h_LX_Mu_Xframe, "LX_Mu_Xframe_samekin1", "X boson traveled distance before producing muon. Frame with X at rest. Same kinematics 1.", Ltxt1, "L", "Events")
PlotCombined(f5.h_LxyX_Mu_Xframe, f3.h_LxyX_Mu_Xframe, f6.h_LxyX_Mu_Xframe, f4.h_LxyX_Mu_Xframe, "LxyX_Mu_Xframe_samekin1", "X boson traveled distance in xy plane before producing muon. Frame with X at rest. Same kinematics 1.", Ltxt1, "L_{xy}", "Events")
PlotCombined(f5.h_LX_El_Xframe, f3.h_LX_El_Xframe, f6.h_LX_El_Xframe, f4.h_LX_El_Xframe, "LX_El_Xframe_samekin1", "X boson traveled distance before producing electron. Frame with X at rest. Same kinematics 1.", Ltxt1, "L", "Events")
PlotCombined(f5.h_LxyX_El_Xframe, f3.h_LxyX_El_Xframe, f6.h_LxyX_El_Xframe, f4.h_LxyX_El_Xframe, "LxyX_El_samekin1", "X boson traveled distance in xy plane before producing electron. Frame with X at rest. Same kinematics 1.", Ltxt1, "L{xy}", "Events")

PlotCombined(f5.h_ptMu, f3.h_ptMu, f6.h_ptMu, f4.h_ptMu, "ptMu_samekin1", "Muon transverse momentum pt. Same kinematics 1.", Ltxt1, "P_{T}", "Events")
PlotCombined(f5.h_ptEl, f3.h_ptEl, f6.h_ptEl, f4.h_ptEl, "ptEl_samekin1", "Electron transverse momentum pt. Same kinematics 1.", Ltxt1, "P_{T}", "Events")
###

### L and Lxy for same kinematics 2
PlotCombined(f1.h_LX_Mu, f7.h_LX_Mu, f2.h_LX_Mu, f8.h_LX_Mu, "LX_Mu_samekin2", "X boson traveled distance before producing muon. Same kinematics 2.", Ltxt2, "L", "Events")
PlotCombined(f1.h_LxyX_Mu, f7.h_LxyX_Mu, f2.h_LxyX_Mu, f8.h_LxyX_Mu, "LxyX_Mu_samekin2", "X boson traveled distance in xy plane before producing muon. Same kinematics 2.", Ltxt2, "L_{xy}", "Events")
PlotCombined(f1.h_LX_El, f7.h_LX_El, f2.h_LX_El, f8.h_LX_El, "LX_El_samekin2", "X boson traveled distance before producing electron. Same kinematics 2.", Ltxt2, "L", "Events")
PlotCombined(f1.h_LxyX_El, f7.h_LxyX_El, f2.h_LxyX_El, f8.h_LxyX_El, "LxyX_El_samekin2", "X boson traveled distance in xy plane before producing electron. Same kinematics 2.", Ltxt2, "L_{xy}", "Events")

PlotCombined(f1.h_LX_Mu_Xframe, f7.h_LX_Mu_Xframe, f2.h_LX_Mu_Xframe, f8.h_LX_Mu_Xframe, "LX_Mu_Xframe_samekin2", "X boson traveled distance before producing muon. Frame with X at rest. Same kinematics 2.", Ltxt2, "L", "Events")
PlotCombined(f1.h_LxyX_Mu_Xframe, f7.h_LxyX_Mu_Xframe, f2.h_LxyX_Mu_Xframe, f8.h_LxyX_Mu_Xframe, "LxyX_Mu_Xframe_samekin2", "X boson traveled distance in xy plane before producing muon. Frame with X at rest. Same kinematics 2.", Ltxt2, "L_{xy}", "Events")
PlotCombined(f1.h_LX_El_Xframe, f7.h_LX_El_Xframe, f2.h_LX_El_Xframe, f8.h_LX_El_Xframe, "LX_El_Xframe_samekin2", "X boson traveled distance before producing electron. Frame with X at rest. Same kinematics 2.", Ltxt2, "L", "Events")
PlotCombined(f1.h_LxyX_El_Xframe, f7.h_LxyX_El_Xframe, f2.h_LxyX_El_Xframe, f8.h_LxyX_El_Xframe, "LxyX_El_samekin2", "X boson traveled distance in xy plane before producing electron. Frame with X at rest. Same kinematics 2.", Ltxt2, "L_{xy}", "Events")

PlotCombined(f1.h_ptMu, f7.h_ptMu, f2.h_ptMu, f8.h_ptMu, "ptMu_samekin2", "Muon transverse momentum pt. Same kinematics 2.", Ltxt2, "P_{T}", "Events")
PlotCombined(f1.h_ptEl, f7.h_ptEl, f2.h_ptEl, f8.h_ptEl, "ptEl_samekin2", "Electron transverse momentum pt. Same kinematics 2.", Ltxt2, "P_{T}", "Events")
###

PlotCombined(f1.h_velocitymagX, f2.h_velocitymagX, f3.h_velocitymagX, f4.h_velocitymagX, "velocitymagX", "X boson speed", Ltxt0, "v", "Events")
PlotCombined(f1.h_velocitymagX_xy, f2.h_velocitymagX_xy, f3.h_velocitymagX_xy, f4.h_velocitymagX_xy, "velocitymagX_xy", "X boxon speed in transverse plane xy", Ltxt0, "v", "Events")


### Time
PlotCombined(f1.h_timeMu_labframe, f2.h_timeMu_labframe, f3.h_timeMu_labframe, f4.h_timeMu_labframe, "timeX_Mu", "X boson time before producing muon", Ltxt0, "t", "Events")
PlotCombined(f1.h_timeEl_labframe, f2.h_timeEl_labframe, f3.h_timeEl_labframe, f4.h_timeEl_labframe, "timeX_El", "X boson time before producing electron", Ltxt0, "t", "Events")
PlotCombined(f1.h_timeMu_Xframe, f2.h_timeMu_Xframe, f3.h_timeMu_Xframe, f4.h_timeMu_Xframe, "timeX_Mu_Xframe", "X boson time before producing muon. Frame with X at rest", Ltxt0, "t", "Events")
PlotCombined(f1.h_timeEl_Xframe, f2.h_timeEl_Xframe, f3.h_timeEl_Xframe, f4.h_timeEl_Xframe, "timeX_El_Xframe", "X boson time before producing electron. Frame with X at rest", Ltxt0, "t", "Events")

### Time same kinematics 1
PlotCombined(f5.h_timeMu_labframe, f3.h_timeMu_labframe, f6.h_timeMu_labframe, f4.h_timeMu_labframe, "timeX_Mu_samekin1", "X boson time before producing muon. Same kinematics 1", Ltxt1, "t", "Events")
PlotCombined(f5.h_timeEl_labframe, f3.h_timeEl_labframe, f6.h_timeEl_labframe, f4.h_timeEl_labframe, "timeX_El_samekin1", "X boson time before producing electron. Same kinematics 1", Ltxt1, "t", "Events")
PlotCombined(f5.h_timeMu_Xframe, f3.h_timeMu_Xframe, f6.h_timeMu_Xframe, f4.h_timeMu_Xframe, "timeX_Mu_Xframe_samekin1", "X boson time before producing muon. Frame with X at rest. Same kinematics 1", Ltxt1, "t", "Events")
PlotCombined(f5.h_timeEl_Xframe, f3.h_timeEl_Xframe, f6.h_timeEl_Xframe, f4.h_timeEl_Xframe, "timeX_El_Xframe_samekin1", "X boson time before producing electron. Frame with X at rest. Same kinematics 1", Ltxt1, "t", "Events")

### Time same kinematics 2
PlotCombined(f1.h_timeMu_labframe, f7.h_timeMu_labframe, f2.h_timeMu_labframe, f8.h_timeMu_labframe, "timeX_Mu_samekin2", "X boson time before producing muon. Same kinematics 2", Ltxt2, "t", "Events")
PlotCombined(f1.h_timeEl_labframe, f7.h_timeEl_labframe, f2.h_timeEl_labframe, f8.h_timeEl_labframe, "timeX_El_samekin2", "X boson time before producing electron. Same kinematics 2", Ltxt2, "t", "Events")
PlotCombined(f1.h_timeMu_Xframe, f7.h_timeMu_Xframe, f2.h_timeMu_Xframe, f8.h_timeMu_Xframe, "timeX_Mu_Xframe_samekin2", "X boson time before producing muon. Frame with X at rest. Same kinematics 2", Ltxt2, "t", "Events")
PlotCombined(f1.h_timeEl_Xframe, f7.h_timeEl_Xframe, f2.h_timeEl_Xframe, f8.h_timeEl_Xframe, "timeX_El_Xframe_samekin2", "X boson time before producing electron. Frame with X at rest. Same kinematics 2", Ltxt2, "t", "Events")
'''


### 2D histograms
if flgck==0:
  TwoDHistogramsDivided4(f1.h_LxyX_VS_dxy_Mu, f2.h_LxyX_VS_dxy_Mu, f3.h_LxyX_VS_dxy_Mu, f4.h_LxyX_VS_dxy_Mu, "Lxy_Vs_dxy", "L_{xy} VS d_{xy} of X boson for Muon production", Ltxt0, "L_{xy} (cm)", "d_{xy} (cm)")
  TwoDHistogramsDivided4(f1.h_IxyX_VS_dxy_Mu, f2.h_IxyX_VS_dxy_Mu, f3.h_IxyX_VS_dxy_Mu, f4.h_IxyX_VS_dxy_Mu, "Ixy_Vs_dxy", "I_{xy} VS d_{xy} of X boson for Muon production", Ltxt0, "I_{xy} (cm)", "d_{xy} (cm)")
  TwoDHistogramsDivided4(f1.h_LxyX_VS_dxyOverSigma_Mu, f2.h_LxyX_VS_dxyOverSigma_Mu, f3.h_LxyX_VS_dxyOverSigma_Mu, f4.h_LxyX_VS_dxyOverSigma_Mu, "Lxy_Vs_dxyOverSigma", "L_{xy} VS d_{xy}/#sigma of X boson for Muon production", Ltxt0, "L_{xy} (cm)", "d_{xy}/#sigma")
  TwoDHistogramsDivided4(f1.h_IxyX_VS_dxyOverSigma_Mu, f2.h_IxyX_VS_dxyOverSigma_Mu, f3.h_IxyX_VS_dxyOverSigma_Mu, f4.h_IxyX_VS_dxyOverSigma_Mu, "Ixy_Vs_dxyOverSigma", "I_{xy} VS d_{xy}/#sigma of X boson for Muon production", Ltxt0, "I_{xy} (cm)", "d_{xy}/#sigma")
  TwoDHistogramsDivided4(f1.h_LxyX_VS_IxyX_Mu, f2.h_LxyX_VS_IxyX_Mu, f3.h_LxyX_VS_IxyX_Mu, f4.h_LxyX_VS_IxyX_Mu, "Lxy_VS_Ixy", "L_{xy} VS I_{xy} for Muon production", Ltxt0, "L_{xy} (cm)", "I_{xy} (cm)")
  TwoDHistogramsDivided4(f1.h_dxy_VS_dxyOverSigma_Mu, f2.h_dxy_VS_dxyOverSigma_Mu, f3.h_dxy_VS_dxyOverSigma_Mu, f4.h_dxy_VS_dxyOverSigma_Mu, "dxy_Vs_dxyOverSigma", "d_{xy} VS d_{xy}/#sigma of X boson for Muon production", Ltxt0, "d_{xy} (cm)", "d_{xy}/#sigma")

  
  TwoDHistogramsDivided4(f1.h_LxyX_VS_dxy_El, f2.h_LxyX_VS_dxy_El, f3.h_LxyX_VS_dxy_El, f4.h_LxyX_VS_dxy_El, "Lxy_Vs_dxy", "L_{xy} VS d_{xy} of X boson for Electron production", Ltxt0, "L_{xy} (cm)", "d_{xy} (cm)")
  TwoDHistogramsDivided4(f1.h_IxyX_VS_dxy_El, f2.h_IxyX_VS_dxy_El, f3.h_IxyX_VS_dxy_El, f4.h_IxyX_VS_dxy_El, "Ixy_Vs_dxy", "I_{xy} VS d_{xy} of X boson for Electron production", Ltxt0, "I_{xy} (cm)", "d_{xy} (cm)")
  TwoDHistogramsDivided4(f1.h_LxyX_VS_dxyOverSigma_El, f2.h_LxyX_VS_dxyOverSigma_El, f3.h_LxyX_VS_dxyOverSigma_El, f4.h_LxyX_VS_dxyOverSigma_El, "Lxy_Vs_dxyOverSigma", "L_{xy} VS d_{xy}/#sigma of X boson for Electron production", Ltxt0, "L_{xy} (cm)", "d_{xy}/#sigma")
  TwoDHistogramsDivided4(f1.h_IxyX_VS_dxyOverSigma_El, f2.h_IxyX_VS_dxyOverSigma_El, f3.h_IxyX_VS_dxyOverSigma_El, f4.h_IxyX_VS_dxyOverSigma_El, "Ixy_Vs_dxyOverSigma", "I_{xy} VS d_{xy}/#sigma of X boson for Electron production", Ltxt0, "I_{xy} (cm)", "d_{xy}/#sigma")
  TwoDHistogramsDivided4(f1.h_LxyX_VS_IxyX_El, f2.h_LxyX_VS_IxyX_El, f3.h_LxyX_VS_IxyX_El, f4.h_LxyX_VS_IxyX_El, "Lxy_VS_Ixy", "L_{xy} VS I_{xy} for Electron production", Ltxt0, "L_{xy} (cm)", "I_{xy} (cm)")
  TwoDHistogramsDivided4(f1.h_dxy_VS_dxyOverSigma_El, f2.h_dxy_VS_dxyOverSigma_El, f3.h_dxy_VS_dxyOverSigma_El, f4.h_dxy_VS_dxyOverSigma_El, "dxy_Vs_dxyOverSigma", "d_{xy} VS d_{xy}/#sigma of X boson for Electron production", Ltxt0, "d_{xy} (cm)", "d_{xy}/#sigma")


### Completing files with multiple histograms
canvas.Print("Combined/All_histograms_{}.pdf]".format(leptselec))
canvas.Print("Combined/All_histograms_Logy_{}.pdf]".format(leptselec))

### Close files

f1.Close()
f2.Close()
f3.Close()
f4.Close()

f5.Close()
f6.Close()
f7.Close()
f8.Close()

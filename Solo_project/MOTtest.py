#    MOT-Player_IndDiff.py
#    Coded by HSM 2020 (Hauke S. Meyerhoff, h.meyerhoff@iwm-tuebingen.de) 
#    and FP 2020 (Frank Papenmeier, frank.papenmeier@uni-tuebingen.de)

#    Copyright 2020 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

#    When using this test, please cite it as: 
#    Meyerhoff, H.S. & Papenmeier, F. (2020). Individual differences in visual 
#    attention: A short, reliable, open source and multilanguage test of 
#    multiple object tracking in PsychoPy. Unpublished Manuscript.  

expMonitorName="MOTtestMonitor"
monitorFPS=60 #Any deviation from 60 Hz requires new motion paths

#params
nTrialsPerBlock=10 
nPracticeTrials=5
nObjects=8 #do not change (more than 8 requires different trial files)
nTargets=4 #do not change (other than 4 not tested)
objDurchmesser=1.3 #Diameter - changes would require different motion paths (or will cause incorrect bouncing)
boxBreite=20 #deg
boxHoehe=20 #deg
recommendedScreenWidthDeg = 30 # do not change (or display will not fit on screen)
recommendedScreenHeightDeg = 22 # do not change (or display will not fit on screen)
 
#Markierungsphase
frameOnsetInterval=0.5
emptyFrameInterval=0.5
markColor=[0,-1,-1]
blinks=4
blinkdur=0.2 #s
blinkpause=0.2 #s
lastblinkdur=0.4 #s

#Instruction
instructionDimension = [30, 20] # x, y, in deg
relativeSizeMainTextInstruction = 0.4
relativeSizeBuffer1 = 0.05
relativeSizeImageInstruction = 0.4
relativeSizeBuffer2 = 0.05
durationPerBlock=3 # in minutes

#additional parameter
freezeInstructionScreensInterval=0.5
infoScreenFreezeInterval=0.5
nInstructionFrames=1
interTrialInterval=1
dataKey = 'd'



####################################################################################
####### TOUCH THE REMAINING CODE ONLY IF YOU KNOW WHAT YOU ARE DOING ###########
####################################################################################

from psychopy import visual, core, event, monitors, gui, tools 
from psychopy.monitors import MonitorCenter
import numpy as np
import sys
import gettext
import os
import collections

# Encoding Hack for Python 2 only
if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')

# ensure working directory is correctly set to the directory this script is located within
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# set preferred language
available_languages = collections.OrderedDict([('English', 'en'), ('Chinese (Simplified)', 'zh_CN'), ('Chinese (Traditional)', 'zh_TW'), ('Danish', 'da'), ('Dutch', 'nl'), ('Finnish', 'fi'), ('French', 'fr'), ('German', 'de'), ('Italian', 'it'), ('Japanese', 'ja'), ('Norwegian', 'no'), ('Polish', 'pl'), ('Portugese', 'pt'), ('Portuguese (Brazil)', 'pt_BR'), ('Russian', 'ru'), ('Spanish', 'es'), ('Swedish', 'sv'), ('Turkish', 'tr')])

# check for config file
lang_cfg = None
try:
    with open('lang.cfg', 'r') as file_lang_cfg:
        lang_cfg = file_lang_cfg.readline()
except:
    pass

if lang_cfg in available_languages.values():
    language = lang_cfg
else: # no config file (with valid data) found -> show GUI dialog
    lang_choices = ['']
    for l in available_languages.keys():
        lang_choices.append(l)

    lang = gui.Dlg(title='Choose Language')
    lang.addField('Language:', choices = lang_choices)
    langData=lang.show()
    while langData is None or not langData[0]:
        error =  gui.Dlg(title='Error Message')
        error.addText('Please choose a language.')
        error.show()
        langData=lang.show()

    language = available_languages[langData[0]]
    
    # save choosen language to config file
    try:
        with open('lang.cfg', 'w') as file_lang_cfg:
            file_lang_cfg.write( language )
    except:
        pass

if language == "en":
    _ = gettext.gettext
else:
    lang = gettext.translation('messages', localedir='locales/translated', languages=[language])
    lang.install()

#Load differnt font for Asian languages (otherwise they appeared cropped on Mac systems in our tests)
fontInstructions = ''
if language == 'zh_CN' or language == 'zh_TW' or language == 'ja':
    fontInstructions='SimSun'

def openMonitorCenter():
    monitorCenter = MonitorCenter.MonitorCenter(0)
    monitorCenter.MainLoop()

monitorScalingFactor = 1.0 #if the monitor (in dva) is smaller than the recommended monitor size - a scaling by this value ensures that the display remains fully visible

# check monitor settings
def checkMonitorSettingsOK(mywin, expMonitorName): # return True if everything is fine, otherwise False
    global monitorScalingFactor
    
    # Bug in PsychoPy with Apple Retina Displays and mouse coordinates when working in degree of visual angle
    # Do not allow to run task on retina displays until bug is fixed within PsychoPy
    if mywin.useRetina:
        mywin.close()
        error =  gui.Dlg(title='Retina Displays not supported', labelButtonOK='Quit', labelButtonCancel='Quit')
        error.addText('Apple Retina Displays are not supported at the moment.\n\nPossible solutions:\n1. Connect an external display to your Macbook and run this task on the external monitor.\n2. Use a different computer to run this task.\n\nNote: There is currently a bug within PsychoPy preventing the use of Retina Displays because PsychoPy reports wrong mouse coordinates on Retina Displays\nwhen running a task in degree of visual angle. Once future versions of PsychoPy resolve this bug, we will allow the use of Retina Displays with respective\nversions of PsychoPy.')
        error.show()
        core.quit() # Currently no possiblity to continue with Retina Displays
    
    # Does monitor exist within PsychoPy Monitor Center?
    if not expMonitorName in monitors.getAllMonitors():
        mywin.close()
        error =  gui.Dlg(title='Monitor does not exist', labelButtonOK='Open PsychoPy Monitor Center', labelButtonCancel='Quit')
        error.addText('You need to add a monitor called \"{monitorname}\" to the PsychoPy Monitor Center in order to run this task.\n\nPlease make sure to enter the correct screen resolution, screen width and screen distance while adding the monitor in the PsychoPy Monitor Center.'.format(monitorname = expMonitorName))
        dlgResponse = error.show()
        if dlgResponse is None: # Cancel Button
            core.quit()
        else: # OK Button
            openMonitorCenter()
            return False # trigger another check of monitor settings whether everyting is OK, now.
    
    # Check monitor settings within PsychoPy Monitor Center
    expMonitor = monitors.Monitor(expMonitorName)
    if expMonitor.getWidth() is None or expMonitor.getDistance() is None or expMonitor.getSizePix()[0] == 0 or expMonitor.getSizePix()[1] == 0:
        mywin.close()
        error =  gui.Dlg(title='Values missing in Monitor Center', labelButtonOK='Open PsychoPy Monitor Center', labelButtonCancel='Quit')
        error.addText('Some values regarding screen resolution, screen width or screen distance are missing in the PsychoPy Monitor Center.\n\nPlease open the PsychoPy Monitor Center and check the values of the monitor called \"{monitorname}\"'.format(monitorname = expMonitorName))
        dlgResponse = error.show()
        if dlgResponse is None: # Cancel Button
            core.quit()
        else: # OK Button
            openMonitorCenter()
            return False # trigger another check of monitor settings whether everyting is OK, now.

    monitorPixelX=expMonitor.getSizePix()[0]
    monitorPixelY=expMonitor.getSizePix()[1]
    frameRate = mywin.getActualFrameRate(nIdentical = 20, nMaxFrames = 120, nWarmUpFrames=5, threshold=1)

#   Commented because check for real resolution does not work on Windows systems that use a scaling different from 100% -> user should make sure to set real resolution of display (irrespective of Windows scaling) into Monitor Center
#    if mywin.size[0] != monitorPixelX or mywin.size[1] != monitorPixelY:
#        mywin.close()
#        error =  gui.Dlg(title='Screen resolution mismatch', labelButtonOK='Open PsychoPy Monitor Center', labelButtonCancel='Quit')
#        error.addText('Mismatch between actual monitor size and the settings in the PsychoPy Monitor Center detected.\n\nActual monitor size found: {width_pixel_actual} x {height_pixel_actual} Pixel\n\nMonitor size according to Monitor Center: {width_pixel_mc} x {height_pixel_mc} Pixel\n\nPlease update the settings of the monitor called \"{monitorname}\" in the PsychoPy Monitor Center to reflect the true monitor resolution.'.format(width_pixel_actual = mywin.size[0], height_pixel_actual = mywin.size[1], width_pixel_mc = monitorSize[0], height_pixel_mc = monitorSize[1], monitorname = expMonitorName))
#        dlgResponse = error.show()
#        if dlgResponse is None: # Cancel Button
#            core.quit()
#        else: # OK Button
#            openMonitorCenter()
#            return False # trigger another check of monitor settings whether everyting is OK, now.
    
    # Does monitor have the requested Frame Rate of 60 Hz?
    if frameRate < 59.5 or frameRate > 60.5:
        mywin.close()
        error =  gui.Dlg(title='Warning', labelButtonOK='Continue anyway', labelButtonCancel='Quit')
        error.addText('This task is designed for monitors running at 60 Hz.\n\nThe following actual framerate was detected: {frame_rate:.2f}\n\nIf you continue anyway, object speeds and trial durations will be wrong.\n\nPossible solution:\nQuit and run this task on an external monitor or differnt computer.'.format(frame_rate = frameRate))
        dlgResponse = error.show()
        if dlgResponse is None: # Cancel Button
            core.quit()
        else: # OK Button
            pass
            
    # Is monitor large enough to display the task at its recommended size?
    width_degrees = round(tools.monitorunittools.pix2deg(monitorPixelX, expMonitor), 2)
    height_degrees = round(tools.monitorunittools.pix2deg(monitorPixelY, expMonitor), 2)
    if width_degrees < recommendedScreenWidthDeg or height_degrees < recommendedScreenHeightDeg:
        mywin.close()
        monitorScalingFactor = min(width_degrees/recommendedScreenWidthDeg, height_degrees/recommendedScreenHeightDeg)
        error =  gui.Dlg(title='Warning', labelButtonOK='Continue with downscaled sizes', labelButtonCancel='Quit')
        error.addText('According to your settings in the PsychoPy Monitor Center, this monitor is smaller than recommended for the presentation of this task.\n\nMonitor size found: {width_degrees} x {height_degrees} degrees of visual angle\n\nMonitor size recommended: {width_degrees_recommended} x {height_degrees_recommended} degrees of visual angle\n\nPossible solutions:\n1. Continue with all sizes being downscaled by the factor {scaling_factor:.3f}\n2. Quit, check your settings in the PsychoPy Monitor Center, and consider reducing the sceen distance.\n3. Quit and run this task on an external monitor or differnt computer.'.format(width_degrees = width_degrees, height_degrees = height_degrees, width_degrees_recommended = recommendedScreenWidthDeg, height_degrees_recommended = recommendedScreenHeightDeg, scaling_factor = monitorScalingFactor))
        dlgResponse = error.show()
        if dlgResponse is None: # Cancel Button
            core.quit()
        else: # OK Button
            pass
    
    return True

while True:
    monitorSize = monitors.Monitor(expMonitorName).getSizePix()
    if monitorSize is None:
        monitorSize = (800,600)
    mywin = visual.Window(monitorSize,color=[-1,-1,-1],monitor=expMonitorName, units="deg", fullscr=True, winType="pyglet", autoLog = False) # create temporaray window to check settings
    checkMonitorSettingsOKResult = checkMonitorSettingsOK(mywin, expMonitorName)
    mywin.close() # ensure temporary window is closed before continue
    if checkMonitorSettingsOKResult == True:
        break


###################################################################
######################### Function Code ###########################
###################################################################

def doTrial(m):
    sz=m.shape
    maus.setVisible(0)
    mywin.flip()
    core.wait(frameOnsetInterval)
    frame.setAutoDraw(True)
    mywin.flip()
    core.wait(emptyFrameInterval)
    
    for dot in dots:
        dot.setAutoDraw(True)
    
    ###Mark Targets
    for i in range(blinks):
        for dot in dots:
            dot.setLineColor(color=[1, 1, 1])
            dot.setFillColor(color=[1, 1, 1])
        
        #white
        for j in range(nObjects):
            dots[j].setPos(newPos=[(m[0,4*j]-boxBreite/2)*monitorScalingFactor, (m[0,4*j+1]-boxHoehe/2)*monitorScalingFactor])

        
        mywin.flip()
        core.wait(blinkpause)
        
        #red
        for j in range(nObjects):
            dot = dots[j]
            if j<4:
                dot.setLineColor(color=markColor)
                dot.setFillColor(color=markColor)
            else:
                dot.setLineColor(color=[1, 1, 1])
                dot.setFillColor(color=[1, 1, 1])
            dot.setPos(newPos=[(m[0,4*j]-boxBreite/2)*monitorScalingFactor, (m[0,4*j+1]-boxHoehe/2)*monitorScalingFactor])
            
        mywin.flip()
        if i==blinks-1:
            core.wait(blinkdur)
        else:
            core.wait(lastblinkdur)

    ### All objects white
    for dot in dots:
        dot.setLineColor(color=[1, 1, 1])
        dot.setFillColor(color=[1, 1, 1])
    
    ### Move objects
    for i in range(sz[0]): 
        for j in range(nObjects):
            dots[j].setPos(newPos=[(m[i,4*j]-boxBreite/2)*monitorScalingFactor,(m[i,4*j+1]-boxHoehe/2)*monitorScalingFactor])
        mywin.flip()

    ### Select targets after motion
    maus.setVisible(1)
    markedObjects=0
    arrayMarkiert=np.zeros((2,nObjects))
    while np.sum(arrayMarkiert[0,:]) <4:
        maus.clickReset()
        # wait for mouse down
        while True:
            buttons = maus.getPressed()
            if buttons[0]==1:
                pos=maus.getPos()
                break
            else:
                mywin.flip()
        for j in range(nObjects):
            arrayMarkiert[1,j]=np.sqrt( (pos[0]-((m[i,4*j]-boxBreite/2)*monitorScalingFactor))*(pos[0]-((m[i,4*j]-boxBreite/2)*monitorScalingFactor))  +  (pos[1]-((m[i,4*j+1]-boxHoehe/2)*monitorScalingFactor))*(pos[1]-((m[i,4*j+1]-boxHoehe/2)*monitorScalingFactor)))
        mindist=np.min(arrayMarkiert[1,:])
        if mindist < objRadius:
            for j in range(nObjects):
                if arrayMarkiert[1,j]==mindist:
                    if arrayMarkiert[0,j]==0:
                        arrayMarkiert[0,j]=1
                    else:
                        arrayMarkiert[0,j]=0
                    break

        #Redraw frame
        for j in range(nObjects):
            dot = dots[j]
            if arrayMarkiert[0,j]==1:
                dot.setLineColor(color=markColor)
                dot.setFillColor(color=markColor)
            else:
                dot.setLineColor(color=[1, 1, 1])
                dot.setFillColor(color=[1, 1, 1])
            dot.setPos(newPos=[(m[i,4*j]-boxBreite/2)*monitorScalingFactor, (m[i,4*j+1]-boxHoehe/2)*monitorScalingFactor])

        mywin.flip()
        
        # wait for mouse release
        while True:
            buttons = maus.getPressed()
            if buttons[0]==0:
                break
            else:
                mywin.flip()
    
    for dot in dots:
        dot.setAutoDraw(False)
    frame.setAutoDraw(False)
    maus.setVisible(0)
    return arrayMarkiert


def getSubjectData():
    info = gui.Dlg(title='Descriptive Data:', labelButtonCancel='Quit')
    info.addField('SubjectID:')
    info.addField('Set:', initial = '1', choices = ['1','2'])
    info.addField('Number of Blocks:', initial = '5', choices = ['1','2','3','4','5'])
    info.addField('Age:')
    info.addField('Gender:')
    info.addField('Handedness:')
    info.addField('Visual Impairment:')
    
    while True:
        vpData=info.show()
        if vpData is None: # Cancel / Quit Button
            core.quit()
        
        subIdExistsAlready = os.path.isfile('results/MOT_sub'+str(vpData[0])+'_'+str(vpData[1])+'.txt')
        
        if not vpData[0] or not vpData[1] or not vpData[2] or not vpData[3] or not vpData[4] or not vpData[5] or not vpData[6] or subIdExistsAlready:
            error =  gui.Dlg(title='Error Message')
            if subIdExistsAlready:
                error.addText('Subject ID already exists.')
            else:
                error.addText('One or more missing values.')
            error.show()
        else:
            break
    
    return vpData
    

def saveData(data, globalTrialCounter, vpData, numBlo, numTrial, nObjects, nTargets, arrayMarkiert,monitorScalingFactor):
    data[globalTrialCounter,0]=vpData[0]
    data[globalTrialCounter,1]=vpData[1]
    data[globalTrialCounter,2]=vpData[2]
    data[globalTrialCounter,3]=vpData[3]
    data[globalTrialCounter,4]=vpData[4]
    data[globalTrialCounter,5]=vpData[5]
    data[globalTrialCounter,6]=vpData[6]
    data[globalTrialCounter,7]=numBlo 
    data[globalTrialCounter,8]=numTrial
    data[globalTrialCounter,9]=nObjects
    data[globalTrialCounter,10]=nTargets
    data[globalTrialCounter,11]=arrayMarkiert[0,0]
    data[globalTrialCounter,12]=arrayMarkiert[0,1]
    data[globalTrialCounter,13]=arrayMarkiert[0,2] 
    data[globalTrialCounter,14]=arrayMarkiert[0,3]
    data[globalTrialCounter,15]=arrayMarkiert[0,4]
    data[globalTrialCounter,16]=arrayMarkiert[0,5]
    data[globalTrialCounter,17]=arrayMarkiert[0,6]
    data[globalTrialCounter,18]=arrayMarkiert[0,7]
    data[globalTrialCounter,19]=np.sum(arrayMarkiert[0,0:4])
    data[globalTrialCounter,20]=monitorFPS
    data[globalTrialCounter,21]=monitorScalingFactor
        
    return data

def saveShortLogfile(subId, data):
    dataShort = np.empty((2,3),dtype="U16")
    dataShort[0,:] = ['subID', 'avTargetsCorrect', 'capacity']
    dataShort[1,0] = subId
    
    #mean number of correctly tracked objects
    sumObjCorrect = 0
    sumObjTotal = 0
    for counter in range (len(data[:,10])-1):
        sumObjCorrect = sumObjCorrect + float(data[1+counter,19])
        sumObjTotal = sumObjTotal + float(data[1+counter,10])
    avTargetCorrect = (sumObjCorrect/sumObjTotal)*nTargets
    observedCapacity = int(data[1,10])*((2*sumObjCorrect/sumObjTotal)-1)
    dataShort[1,1] = avTargetCorrect
    dataShort[1,2] = observedCapacity
    np.savetxt('results/MOT_sub'+str(vpData[0])+'_'+str(vpData[1])+'_short.txt', dataShort, delimiter=";", fmt="%s")
    
    return observedCapacity


def showInfoScreen(content, freezeInterval, content2=_('Press any key to continue'), content3=''):
    text.setText(content)
    text.setPos([0,3*monitorScalingFactor])
    text.draw()
    text.setText(content2)
    text.setPos([0,-8*monitorScalingFactor])
    text.draw() 
    text.setText(content3)
    text.setPos([0,0])
    text.draw()
    mywin.flip()
    core.wait(freezeInterval)
    waitForAnyKey()
    mywin.flip()
    core.wait(interTrialInterval)


def showInstructions(mywin, number_duration_minutes):
    
    instrMainText = _('Dear participant,')
    instrMainText = instrMainText + '\n\n'
    instrMainText = instrMainText + _('The following test will take approximately {number_duration_minutes} minutes. The test is divided into several trials between which you may take short breaks. At first, however, there are five practice trials. The following example explains your task.').format(number_duration_minutes = number_duration_minutes)
    instrMainText = instrMainText + '\n\n'
    instrMainText = instrMainText + _('At the beginning of every trial, eight discs appear on the screen. Four of them repeatedly flash red. Your task is to follow these discs throughout their phase of movement and to select them with a mouse click when they come to a stop.')
    instrMainText = instrMainText + '\n'
    
    instructionDimension[0] = instructionDimension[0]*monitorScalingFactor
    instructionDimension[1] = instructionDimension[1]*monitorScalingFactor
    
    #Select appropriate Letter size
    instructionLetterSize = 0.05 
    while True:
        instrU1 = visual.TextStim(mywin, height=instructionLetterSize, wrapWidth=instructionDimension[0], units = 'deg', font=fontInstructions)
        instrU1.setText(instrMainText)

        if tools.monitorunittools.pix2deg(instrU1.boundingBox[1], mywin.monitor) < instructionDimension[1]*relativeSizeMainTextInstruction:
            instructionLetterSize = instructionLetterSize + 0.05
        else:
            instructionLetterSize = instructionLetterSize - 0.05
            instrU1 = visual.TextStim(mywin,height=instructionLetterSize, wrapWidth=instructionDimension[0], units = 'deg', font=fontInstructions)
            instrU1.setText(instrMainText)
            break
    instrU1.setPos([0, instructionDimension[1]/2 - (instructionDimension[1]*relativeSizeMainTextInstruction/2)])
    instrU1.draw()

    #Place image with correctness-text inside
    pngParadigm = visual.ImageStim(mywin, "illustrationParadigm.png", units="deg")
    pngParadigm.size = [(instructionDimension[1]*relativeSizeImageInstruction/pngParadigm.size[1])*pngParadigm.size[0],(instructionDimension[1]*relativeSizeImageInstruction/pngParadigm.size[1])*pngParadigm.size[1]]
    pngParadigm.setPos([0,(instrU1.pos[1]-tools.monitorunittools.pix2deg(instrU1.boundingBox[1]/2.0, mywin.monitor)-pngParadigm.size[1]/2.0-relativeSizeBuffer1*instructionDimension[1])])
    pngParadigm.draw()
    
    paradigmFeedbackText = visual.TextStim(mywin, height=pngParadigm.size[1]/18, wrapWidth=instructionDimension[0], color=(-1,-1,-1), units = 'deg', font=fontInstructions)
    paradigmFeedbackText.setPos([(pngParadigm.pos[0]+(pngParadigm.size[0]/2.85)),pngParadigm.pos[1]])
    paradigmFeedbackText.setText(_('{numcorrect} out of 4 correct').format(numcorrect = 4))
    paradigmFeedbackText.draw()
    
    #Place lower text
    instrL1 = visual.TextStim(mywin, height=instructionLetterSize, wrapWidth=instructionDimension[0], units = 'deg', font=fontInstructions)
    instrL1.setText(_('If you should have any questions please turn to the test conductor now.'))
    instrL1.setPos([0,pngParadigm.pos[1]-pngParadigm.size[1]/2-tools.monitorunittools.pix2deg(instrL1.boundingBox[1]/2, mywin.monitor)-relativeSizeBuffer2*instructionDimension[1]])
    instrL1.draw()
    
    instrL2 = visual.TextStim(mywin, height=instructionLetterSize, wrapWidth=instructionDimension[0], units = 'deg', font=fontInstructions)
    instrL2.setText(_('-- Press any key to start --'))
    instrL2.setPos([0,instructionDimension[1]/(-2)])
    instrL2.draw()
    
    mywin.flip()
    core.wait(freezeInstructionScreensInterval)
    waitForAnyKey()
    mywin.flip()

def showFinalScreen(content, freezeInterval, content2=_('Press any key to continue'), content3='', observedCapacity=''):
    text.setText(content)
    text.setPos([0,3*monitorScalingFactor])
    text.draw()
    text.setText(content2)
    text.setPos([0,-8*monitorScalingFactor])
    text.draw() 
    text.setText(content3)
    text.setPos([0,0])
    text.draw()
    mywin.flip()
    core.wait(freezeInterval)
    keyPressed = waitForAnyKey()
    if keyPressed == dataKey:
        showInfoScreen(content=_('Observed Tracking Capacity'), freezeInterval=2, content2=_('Press any key to quit'), content3=str(np.round(observedCapacity,2)))
    else:
        mywin.flip()
        core.wait(interTrialInterval)

def waitForAnyKey():
    event.clearEvents()
    while True:
        a = event.getKeys(timeStamped = True)
        if len(a)>0: 
            if a[0][0]=='q':
                event.clearEvents()
                while True:
                    a = event.getKeys(timeStamped = True)
                    if len(a)>0: 
                        if a[0][0]=='u':
                            event.clearEvents()
                            while True:
                                a = event.getKeys(timeStamped = True)
                                if len(a)>0: 
                                    if a[0][0]=='i':
                                        event.clearEvents()
                                        while True:
                                            a = event.getKeys(timeStamped = True)
                                            if len(a)>0: 
                                                if a[0][0]=='t':
                                                    maus.setVisible(1)
                                                    mywin.close()
                                                    core.quit()
                                                else:
                                                    break
                                    break
                        break
            break
    #event.clearEvents()
    return a[0][0]




###################################################################
###################### Experiment Code ###########################
###################################################################
vpData=getSubjectData()

### Logfile
nBlocks = int(vpData[2])
dataHeader=['subject','set', 'nBlocksTotal','age','sex','handedness','visionImpairment','block','trial','nObjects','nTargets','o1marked','o2marked','o3marked','o4marked','o5marked','o6marked','o7marked','o8marked','sumCorrect','fps','monitorScalingFactor']
data = np.empty((nTrialsPerBlock*nBlocks+1,len(dataHeader)),dtype='U16')
data[0,:]=dataHeader

### Objects and variables
globalTrialCounter=1
objRadius = objDurchmesser/2.0*monitorScalingFactor
monitorSize = monitors.Monitor(expMonitorName).getSizePix()
mywin = visual.Window(monitorSize,color=[-1,-1,-1],monitor=expMonitorName, units="deg", fullscr=True, winType="pyglet", autoLog = False) # create experimental window
maus=event.Mouse()
maus.setVisible(0)

dots = []
for j in range(nObjects):
    cur_dot = visual.Circle(mywin, radius=objRadius)
    dots.append(cur_dot)

frame = visual.Rect(mywin, width=boxBreite*monitorScalingFactor, height=boxHoehe*monitorScalingFactor)
frame.setLineColor=[1,1,1]
text = visual.TextStim(mywin, pos=[0,3],height=1.5*monitorScalingFactor, wrapWidth=40, font=fontInstructions)
instr = visual.TextStim(mywin, pos=[0,3],height=1.5, wrapWidth=20, font=fontInstructions)


#instructions
number_duration_minutes = nBlocks*durationPerBlock
showInstructions(mywin, number_duration_minutes)

#practice trials
showInfoScreen(_('Practice'), infoScreenFreezeInterval)
for nPra in range(nPracticeTrials):
    m = np.loadtxt('motionPaths_' + str(int(monitorFPS))+ 'Hz/set' + str(vpData[1])+'/practice/trial'+str(int(nPra+1))+'.txt', delimiter=";")
    arrayMarkiert=doTrial(m)
    tarCorrect = np.sum(arrayMarkiert[0,0:4])
    showInfoScreen(_('{numcorrect} out of 4 correct').format(numcorrect = int(tarCorrect)), infoScreenFreezeInterval)

# Block- and Trial-Loop
showInfoScreen(_('Start of the test'), infoScreenFreezeInterval)
for numBlo in range(nBlocks):
    showInfoScreen(_('Block {curblock} of {numblocks}').format(curblock = (numBlo+1), numblocks = nBlocks), infoScreenFreezeInterval)
    
    #Load trial
    for numTrial in range(nTrialsPerBlock):
        m = np.loadtxt('motionPaths_' + str(int(monitorFPS))+ 'Hz/set' + str(vpData[1])+'/block' + str(int(numBlo+1))+ '/trial'+str(int(numTrial+1))+'.txt', delimiter=";")
        
        #Run trial
        arrayMarkiert=doTrial(m)
             
        #Log data
        data = saveData(data, globalTrialCounter, vpData, numBlo, numTrial, nObjects, nTargets, arrayMarkiert, monitorScalingFactor)
        globalTrialCounter = globalTrialCounter+1
        
        #Provide feedback
        tarCorrect = np.sum(arrayMarkiert[0,0:4])
        showInfoScreen(_('{numcorrect} out of 4 correct').format(numcorrect = int(tarCorrect)), infoScreenFreezeInterval)

### Finishing Experiment
np.savetxt('results/MOT_sub'+str(vpData[0])+'_'+str(vpData[1])+'.txt', data, delimiter=";", fmt="%s", encoding='utf-8')
observedCapacity = saveShortLogfile(vpData[0], data)
showFinalScreen(_('End of the test'), 2, _('Please contact the test administrator'), "",observedCapacity)
maus.setVisible(1)
mywin.close()
core.quit()
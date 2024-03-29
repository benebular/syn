#double check you have the packages below installed, some have dependencies
from psychopy import visual, core, event, data
import csv, random, pyxid, time, os

experiment_dir = '/Users/benlang/Documents/GitHub/syn/' #makes a variable that is the experiment directory
os.chdir(experiment_dir) #tells the os to go to the directory every time

'''....................Stimtracker...........................................'''
# This sets the Cedrus StimTracker box in order to send the triggers

# class NullStimtracker(object):
#     def activate_line(self, bitmask=None):
#         pass
#
# # Looks for stimtracker hardware, if not found: sends a warning
# def get_stimtracker(trigger_duration=5):
#     for dev in pyxid.get_xid_devices():
#         if dev.is_stimtracker():
#             dev.set_pulse_duration(trigger_duration)
#             return dev
#     print "STIMTRACKER NOT FOUND!"
#     decision=raw_input('Continue anyway? [y/n]: ')
#     if decision=='y':
#         return NullStimtracker()
#     else:
#         core.quit() #you'll have to hit enter after this and then it will prompt the above question
#
# triggerBox = get_stimtracker() #run the function above, saving stimtracker as triggerBox
#


'''.................... Experiment and Participant info ......................'''
expInfo={}
expInfo['Participant']= raw_input('Participant: ')
expInfo['Run']=raw_input('Prac-Expt: ')
#hit enter after these three lines and then it will ask you to put in the info, will only record if experiment actually runs


'''.................... Create experiment objects ..........................'''
#creates the different parts of the presentation screen and the experiment as objects
#win is the window/figure
#word is the text in the center screen
#fixation is the fixation cross int eh center screen
#instructions is the text for just the present_instructions
#photodiode creates a square stimulus at the top right corner to present and trigger the photo diode
#rtClock creates an object that will be used to record the time of a given response, object is the time, the object then gets inserted into the class so every time it's used, it records the time

win = visual.Window(monitor="testMonitor", units="pix", fullscr=True, colorSpace='rgb255', color=[127,127,127])
word = visual.TextStim(win,text='', font='Courier New', wrapWidth=900, alignHoriz='center', height=40, color=(-1,-1,-1))
fixation = visual.TextStim(win, text='+', height=40, color=(-1,-1,-1))
instructions = visual.TextStim(win,text='', font='Courier New', wrapWidth=800, alignHoriz='center', height=30, color=(-1,-1,-1))
photodiode = visual.Rect(win, width=90, height=90, pos=[510,360], fillColor=[255,255,255], fillColorSpace='rgb255')
rtClock = core.Clock()

win.mouseVisible = False #This hides the mouse.



'''........................... Functions ....................................'''
# Presenting instructions to the screen.
# When using this, edit "text=''" to contain your instructions
def present_instructions(text=''):
    instructions.setText(text)
    instructions.draw()
    win.flip()
    return event.waitKeys(keyList=['9','q'], timeStamped=rtClock) #This waits for "1" to continue, edit if need other buttons


def present_fix():
    for frame in range (36): #600ms, draws fixation for 300ms then blank for 300ms
        if frame <= 18:
            fixation.draw()
        win.flip()
        # return event.waitKeys(keyList=['1'])

# Presents a word that stays on screen until response
def present_word(text='', trigger=None, photoDiode=True):
    word.setText(text)
    if trigger is not None:
        win.callOnFlip(triggerBox.activate_line, bitmask=int(trigger))
    win.callOnFlip(rtClock.reset)
    word.draw()
    if photoDiode:
        photodiode.draw()
    win.flip()
    return event.waitKeys(keyList=['1', 'q'], timeStamped=rtClock)


def make_blocks(stim, n):
    # Creates n blocks from stim. nb stim must be dividable by n.
    # no back to back repeats by default, because unique targets in each block

    # ADD BACK TO BACK REPEAT CHECK IN TEMPLATE.
    out = []
    for j in range(0, len(stim), len(stim)/n):
            out.append(stim[j:j+len(stim)/n])
    for i in out:
        random.shuffle(i)
    return out



'''.......................Experiment starts here..............................'''

##---------------------------Practice-------------------------------------##
if expInfo['Run'] == 'Prac':

    with open('mri_practice.csv') as f:
        trials_practice = [i for i in csv.DictReader(f)]

    present_instructions('You will start the practice now. Please read each sentence of four words aloud and speak at a casual pace.')

    for trial in trials_practice:
        present_fix()
        text = '%s %s %s %s' %(trial['w1'],trial['w2'],trial['w3'],trial['w4'])
        resp = present_word(text=text, photoDiode=False) #present target
        if resp[0][0] == 'q':
            win.close()
            core.quit()
        resp2 = present_instructions('Great job! Please wait while we set up the next sentence.')
        if resp2[0][0]=='q':
            win.close()
            core.quit()
        win.flip()

    present_instructions('The practice is over.')

##---------------------------Experiment-------------------------------------##

elif expInfo['Run'] == 'Expt':

    with open('mri_stimuli.csv') as f:
        trials_practice = [i for i in csv.DictReader(f)]

    exp = data.ExperimentHandler(dataFileName='%s_logfile' %expInfo['Participant'], autoLog=False, savePickle=False)

    present_instructions('You will start the experiment now. Please read each sentence of four words aloud and speak at a casual pace.')

    trialnum = 0
    for trial in trials_practice:
        present_fix()
        text = '%s %s %s %s' %(trial['w1'],trial['w2'],trial['w3'],trial['w4'])
        resp = present_word(text=text, photoDiode=False) #present target
        present_instructions('Great job! Please wait while we set up the next sentence.')
        win.flip()
        if resp[0][0] == 'q':
            win.close()
            core.quit()

        trialnum += 1

        exp.addData('participant', expInfo['Participant'])
        exp.addData('trialnum', trialnum)
        exp.addData('text', text)
        exp.addData('RT', resp[0][1])
        exp.nextEntry()

    present_instructions('The experiment is over. Please lie still for a moment while we come to take you out of the MRI.')





# Fix coming part



##-------------------------Experiment------------------------------------##
# elif expInfo['Run'] == 'Expt':
#     #Importing stimuli
#     with open('mri_stimuli.csv') as f:
#         trials = [i for i in csv.DictReader(f)]
#
#     exp = data.ExperimentHandler(dataFileName='%s_logfile' %expInfo['Participant'], autoLog=False, savePickle=False)
#
#     present_instructions('Lexical decision task: index (2) for words, middle finger (1) for non words.')
#
#     #randomize and block the trials
#     random.shuffle(trials)
#     blocks = make_blocks(trials,4) #4 blocks in this case
#     trialnum = 0
#     blocknum = 0
#     for block in blocks:
#         if blocknum > 0:
#             prompt = 'You have completed block #'+str(blocknum)+". Take a break, then press 1 when you are ready to continue."
#             present_instructions(prompt)
#
#         for trial in block:
#             present_fix()
#             resp = present_word(text=trial['target'])
#             win.flip()
#             if resp[0][0] == 'q':
#                 win.close()
#                 core.quit()
#             core.wait(random.gauss(1.0,0.167)) #isi
#             trialnum += 1
#
#             exp.addData('participant', expInfo['Participant'])
#             exp.addData('trialnum', trialnum)
#             exp.addData('target', trial['target'])
#             exp.addData('target_type', trial['target_type'])
#             exp.addData('trigger', trial['trigger'])
#             exp.addData('RT', resp[0][1])
#             exp.nextEntry()
#
#         blocknum += 1
# #
#     present_instructions('The experiment is over. Thank you.')
#
win.close()
core.quit()

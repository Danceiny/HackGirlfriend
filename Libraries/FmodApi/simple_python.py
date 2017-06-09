# -*- coding: utf-8
# We don’t have an official Python wrapper over FMOD, but Python supports calling into dynamic libraries with ctypes. We’ll show you a really simple example that works in both Python 2.7 and Python 3.4 on windows, for both 32 and 64 bit versions.
#
# Download the latest Programmers API from the FMOD download page. We’ve written this example assuming version 1.07.06. You might need to adjust the script if you get a later version.
#
# Navigate to the programmers API directory and create a new directory. Copy the .dll files and the .bank files in to your directory from here:
#
# \FMOD Studio API Windows 1.07.06\api\lowlevel\lib
# \FMOD Studio API Windows 1.07.06\api\studio\lib
# \FMOD Studio API Windows 1.07.06\api\studio\examples\media
#
# Your new directory should have a bunch of .dll files and all the example banks in it. Now create a new python file in your new directory, call it simple_python.py. We want to import a few libraries, define a helper function, and set up some constants:


from ctypes import *
import time

PLATFORM_SUFFIX = "64" if sizeof(c_voidp) == 8 else ""

# Version：1.09.04
VERSION = 0x00010904

BANK_FILES = [ "Master Bank.bank", "Master Bank.strings.bank", "Weapons.bank" ]

studio_dll = None
studio_sys = None

def check_result(r):
    if r != 0:
        print("ERROR: Got FMOD_RESULT {0}".format(r))


# Now we can define a function to initialize FMOD Studio and set up the logging build. We can call any FMOD function using ctypes. There are some constants which we just have to hard code:
def studio_init():
    print("Initializing FMOD Studio");
    global studio_dll
    global studio_sys
    studio_dll = WinDLL("fmodstudioL" + PLATFORM_SUFFIX)
    lowlevel_dll = WinDLL("fmodL" + PLATFORM_SUFFIX)
    # Write debug log to file
    check_result(lowlevel_dll.FMOD_Debug_Initialize(0x00000002, 1, 0, "log.txt".encode('ascii')))
    # Create studio system
    studio_sys = c_voidp()
    check_result(studio_dll.FMOD_Studio_System_Create(byref(studio_sys), VERSION))
    # Call System init
    check_result(studio_dll.FMOD_Studio_System_Initialize(studio_sys, 256, 0, 0, c_voidp()))
    # Load banks
    for bankname in BANK_FILES:
        print("Loading bank: " + bankname)
        bank = c_voidp()
        check_result(studio_dll.FMOD_Studio_System_LoadBankFile(studio_sys, bankname.encode('ascii'), 0, byref(bank)))


# The above code loads the FMOD dynamic libraries and initializes FMOD, then loads a few of the example banks.
#
# We’ll add a function to play a sound. It creates an event instance, starts it, then releases the handle, which means the event will be cleaned up when it finishes making sound.
def play_sound(soundname):
    print("Playing sound: " + soundname)
    event_desc = c_voidp()
    check_result(studio_dll.FMOD_Studio_System_GetEvent(studio_sys, soundname.encode('ascii'), byref(event_desc)))
    event_inst = c_voidp()
    check_result(studio_dll.FMOD_Studio_EventDescription_CreateInstance(event_desc, byref(event_inst)))
    check_result(studio_dll.FMOD_Studio_EventInstance_SetVolume(event_inst, c_float(0.75)))
    check_result(studio_dll.FMOD_Studio_EventInstance_Start(event_inst))
    check_result(studio_dll.FMOD_Studio_EventInstance_Release(event_inst))
# Next we’ll define a function to tick FMOD Studio. In the case of this script we’ll just sleep in the script for a while to let the sound play out.

def tick_update():
    print("Updating...")
    for loop in range(0, 100):
        check_result(studio_dll.FMOD_Studio_System_Update(studio_sys))
        time.sleep(0.050)
# Now we can call our functions one after another:

studio_init()
play_sound("event:/Explosions/Single Explosion")
tick_update()
# If you run the python script it should load banks and play events. If you are missing files or mismatched versions, it may print an error instead. It should also write out a file log.txt with more information.
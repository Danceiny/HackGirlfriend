# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from ctypes import *
import time
import os
# PLATFORM_SUFFIX = "64" if sizeof(c_voidp) == 8 else ""
#
# # Version：1.09.04
# VERSION = 0x00010904

FMOD_DEFAULT=0x00000000  #/* Default for all modes listed below. FMOD_LOOP_OFF, FMOD_2D, FMOD_3D_WORLDRELATIVE, FMOD_3D_INVERSEROLLOFF */
FMOD_LOOP_OFF=0x00000001  #/* For non looping sounds. (DEFAULT).  Overrides FMOD_LOOP_NORMAL / FMOD_LOOP_BIDI. */
#define FMOD_LOOP_NORMAL               0x00000002  /* For forward looping sounds. */
#define FMOD_LOOP_BIDI                 0x00000004  /* For bidirectional looping sounds. (only works on software mixed static sounds). */
#define FMOD_2D                        0x00000008  /* Ignores any 3d processing. (DEFAULT). */
#define FMOD_3D                        0x00000010  /* Makes the sound positionable in 3D.  Overrides FMOD_2D. */
#define FMOD_CREATESTREAM              0x00000080  /* Decompress at runtime, streaming from the source provided (ie from disk).  Overrides FMOD_CREATESAMPLE and FMOD_CREATECOMPRESSEDSAMPLE.  Note a stream can only be played once at a time due to a stream only having 1 stream buffer and file handle.  Open multiple streams to have them play concurrently. */
#define FMOD_CREATESAMPLE              0x00000100  /* Decompress at loadtime, decompressing or decoding whole file into memory as the target sample format (ie PCM).  Fastest for playback and most flexible.  */
#define FMOD_CREATECOMPRESSEDSAMPLE    0x00000200  /* Load MP2/MP3/IMAADPCM/Vorbis/AT9 or XMA into memory and leave it compressed.  Vorbis/AT9 encoding only supported in the FSB file format.  During playback the FMOD software mixer will decode it in realtime as a 'compressed sample'.  Overrides FMOD_CREATESAMPLE.  If the sound data is not one of the supported formats, it will behave as if it was created with FMOD_CREATESAMPLE and decode the sound into PCM. */
#define FMOD_OPENUSER                  0x00000400  /* Opens a user created static sample or stream. Use FMOD_CREATESOUNDEXINFO to specify format and/or read callbacks.  If a user created 'sample' is created with no read callback, the sample will be empty.  Use Sound::lock and Sound::unlock to place sound data into the sound if this is the case. */
#define FMOD_OPENMEMORY                0x00000800  /* "name_or_data" will be interpreted as a pointer to memory instead of filename for creating sounds.  Use FMOD_CREATESOUNDEXINFO to specify length.  If used with FMOD_CREATESAMPLE or FMOD_CREATECOMPRESSEDSAMPLE, FMOD duplicates the memory into its own buffers.  Your own buffer can be freed after open.  If used with FMOD_CREATESTREAM, FMOD will stream out of the buffer whose pointer you passed in.  In this case, your own buffer should not be freed until you have finished with and released the stream.*/
#define FMOD_OPENMEMORY_POINT          0x10000000  /* "name_or_data" will be interpreted as a pointer to memory instead of filename for creating sounds.  Use FMOD_CREATESOUNDEXINFO to specify length.  This differs to FMOD_OPENMEMORY in that it uses the memory as is, without duplicating the memory into its own buffers.  Cannot be freed after open, only after Sound::release.   Will not work if the data is compressed and FMOD_CREATECOMPRESSEDSAMPLE is not used. */
#define FMOD_OPENRAW                   0x00001000  /* Will ignore file format and treat as raw pcm.  Use FMOD_CREATESOUNDEXINFO to specify format.  Requires at least defaultfrequency, numchannels and format to be specified before it will open.  Must be little endian data. */
#define FMOD_OPENONLY                  0x00002000  /* Just open the file, dont prebuffer or read.  Good for fast opens for info, or when sound::readData is to be used. */
#define FMOD_ACCURATETIME              0x00004000  /* For System::createSound - for accurate Sound::getLength/Channel::setPosition on VBR MP3, and MOD/S3M/XM/IT/MIDI files.  Scans file first, so takes longer to open. FMOD_OPENONLY does not affect this. */
#define FMOD_MPEGSEARCH                0x00008000  /* For corrupted / bad MP3 files.  This will search all the way through the file until it hits a valid MPEG header.  Normally only searches for 4k. */
#define FMOD_NONBLOCKING               0x00010000  /* For opening sounds and getting streamed subsounds (seeking) asyncronously.  Use Sound::getOpenState to poll the state of the sound as it opens or retrieves the subsound in the background. */
#define FMOD_UNIQUE                    0x00020000  /* Unique sound, can only be played one at a time */
#define FMOD_3D_HEADRELATIVE           0x00040000  /* Make the sound's position, velocity and orientation relative to the listener. */
#define FMOD_3D_WORLDRELATIVE          0x00080000  /* Make the sound's position, velocity and orientation absolute (relative to the world). (DEFAULT) */
#define FMOD_3D_INVERSEROLLOFF         0x00100000  /* This sound will follow the inverse rolloff model where mindistance = full volume, maxdistance = where sound stops attenuating, and rolloff is fixed according to the global rolloff factor.  (DEFAULT) */
#define FMOD_3D_LINEARROLLOFF          0x00200000  /* This sound will follow a linear rolloff model where mindistance = full volume, maxdistance = silence. */
#define FMOD_3D_LINEARSQUAREROLLOFF    0x00400000  /* This sound will follow a linear-square rolloff model where mindistance = full volume, maxdistance = silence. */
#define FMOD_3D_INVERSETAPEREDROLLOFF  0x00800000  /* This sound will follow the inverse rolloff model at distances close to mindistance and a linear-square rolloff close to maxdistance. */
#define FMOD_3D_CUSTOMROLLOFF          0x04000000  /* This sound will follow a rolloff model defined by Sound::set3DCustomRolloff / Channel::set3DCustomRolloff.  */
#define FMOD_3D_IGNOREGEOMETRY         0x40000000  /* Is not affect by geometry occlusion.  If not specified in Sound::setMode, or Channel::setMode, the flag is cleared and it is affected by geometry again. */
from enum import Enum
Month = Enum('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

EFFECT_TYPE = Enum('MODE_NORMAL','MODE_LUOLI','MODE_DASHU','MODE_JINGSONG','MODE_GUOGUAI','MODE_KONGLING')

class FmodHelper:
    def __init__(self):
        self.LIB_PATH = '../../Libraries/FmodApi/'
        self.VERSION = 0x00010904
        self.PLATFORM_SUFFIX = "64" if sizeof(c_voidp) == 8 else ""
        self.BANK_FILES = [ "Master Bank.bank", "Master Bank.strings.bank", "Weapons.bank" ]
        self.studio_dll = None
        self.studio_sys = None

    def studio_init(self):
        print("Initializing FMOD Studio")
        os.chdir(self.LIB_PATH)
        self.studio_dll = WinDLL(r"fmodstudioL" + self.PLATFORM_SUFFIX)
        self.lowlevel_dll = WinDLL(r"fmodL" + self.PLATFORM_SUFFIX)
        # Write debug log to file
        self.check_result(self.lowlevel_dll.FMOD_Debug_Initialize(0x00000002, 1, 0, "log.txt".encode('ascii')))
        # Create studio system
        self.studio_sys = c_voidp()
        self.check_result(self.studio_dll.FMOD_Studio_System_Create(byref(self.studio_sys), self.VERSION))
        # Call System init
        self.check_result(self.studio_dll.FMOD_Studio_System_Initialize(self.studio_sys, 256, 0, 0, c_voidp()))



    def load_banks(self,bank_files):
        # Load banks
        for bankname in bank_files:
            print("Loading bank: " + bankname)
            bank = c_voidp()
            self.check_result(
                self.studio_dll.FMOD_Studio_System_LoadBankFile(self.studio_sys, bankname.encode('ascii'), 0, byref(bank)))

        # //音效类型 大叔萝莉什么的类型
        # self.MODE_NORMAL=0
        # self.MODE_LUOLI=1
        # self.MODE_DASHU=2
        # self.MODE_JINGSONG=3
        # self.MODE_GAOGUAI=4
        # self.MODE_KONGLING=5
    # /**
    #  * 音效处理传2个值
    #  * @param path 音频文件路径
    #  * @param type 音频文件类型
    #  */
    def fix(self,origin_voice_path,type):
        # 创建声音

        # FMOD_RESULT
        # F_API
        # FMOD_System_CreateSound(FMOD_SYSTEM * system, const
        # char * name_or_data, FMOD_MODE
        # mode, FMOD_CREATESOUNDEXINFO * exinfo, FMOD_SOUND ** sound);
        fmod_sound = c_voidp()
        exinfo = c_voidp()
        event_desc = c_voidp()
        self.lowlevel_dll.FMOD_System_CreateSound(self.studio_sys,origin_voice_path.encode('ascii'),FMOD_DEFAULT,exinfo,fmod_sound)

        if type==EFFECT_TYPE.MODE_NORMAL:
            pass
        if type==EFFECT_TYPE.MODE_LUOLI:
            pass

    def check_result(self,r):
        if r != 0:
            print("ERROR: Got FMOD_RESULT {0}".format(r))

    def tick_update(self):
        print("Updating...")
        for loop in range(0, 100):
            self.check_result(self.studio_dll.FMOD_Studio_System_Update(self.studio_sys))
            time.sleep(0.050)

    def play_sound(self,soundname):
        print("Playing sound: " + soundname)
        event_desc = c_voidp()
        self.check_result(self.studio_dll.FMOD_Studio_System_GetEvent(self.studio_sys, soundname.encode('ascii'), byref(event_desc)))
        event_inst = c_voidp()
        self.check_result(self.studio_dll.FMOD_Studio_EventDescription_CreateInstance(event_desc, byref(event_inst)))
        self.check_result(self.studio_dll.FMOD_Studio_EventInstance_SetVolume(event_inst, c_float(0.75)))
        self.check_result(self.studio_dll.FMOD_Studio_EventInstance_Start(event_inst))
        self.check_result(self.studio_dll.FMOD_Studio_EventInstance_Release(event_inst))


helper = FmodHelper()
helper.studio_init()
# helper.play_sound("event:/Explosions/Single Explosion")
helper.fix('voice.mp3','')
helper.tick_update()

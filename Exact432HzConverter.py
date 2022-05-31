import numpy as np
from pydub import AudioSegment
from pydub.utils import mediainfo
#from tkinter import *
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
from tkinter import NO, DISABLED, NORMAL
import glob
import os
import threading

#print("Exact 432Hz Converter v1.2")
#print("Author: CardLin")
#print("")

# The frequency of 440hz tuning
tone_freq=[16.35,17.32,18.35,19.45,20.6,21.83,23.12,24.5,25.96,27.5,29.14,30.87,32.7,34.65,36.71,38.89,41.2,43.65,46.25,49,51.91,55,58.27,61.74,65.41,69.3,73.42,77.78,82.41,87.31,92.5,98,103.83,110,116.54,123.47,130.81,138.59,146.83,155.56,164.81,174.61,185,196,207.65,220,233.08,246.94,261.63,277.18,293.66,311.13,329.63,349.23,369.99,392,415.3,440,466.16,493.88,523.25,554.37,587.33,622.25,659.25,698.46,739.99,783.99,830.61,880,932.33,987.77,1046.5,1108.73,1174.66,1244.51,1318.51,1396.91,1479.98,1567.98,1661.22,1760,1864.66,1975.53,2093,2217.46,2349.32,2489.02,2637.02,2793.83,2959.96,3135.96,3322.44,3520,3729.31,3951.07,4186.01,4434.92,4698.63,4978.03,5274.04,5587.65,5919.91,6271.93,6644.88,7040,7458.62,7902.13]
tone_freq = np.array(tone_freq) 

# Generate frequency of each tuning
tones={}
for frequency in np.arange(424.0, 448.1, 0.10):
    tones[str(frequency)]=tone_freq*frequency/440.0

# Speed change function
def speed_change(sound, speed=1.0, target_sample_rate=48000):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)
      })
     # convert the sound with altered frame rate to a standard frame rate
     # so that regular playback programs will work right. They often only
     # know how to play audio at standard frame rate (like 44.1k)
    #return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)
    return sound_with_altered_frame_rate.set_frame_rate(target_sample_rate)

def analyze_tone(song):
    sample_rate = song.frame_rate
    duration = song.duration_seconds
    # Handle the audio which duration smaller than 100 sec
    if duration<101:
        pad_ms = int((120.0-duration)*1000)
        silence = AudioSegment.silent(duration=pad_ms)
        audio = song + silence
    else:
        audio = song
    
    # Get first 100 second of the audio
    first_100_second = audio[:100*1000]
    mono_first_100_second = first_100_second.set_channels(1) #Mono
    
    # Get raw data (samples) and FFT parameter
    samples = mono_first_100_second.get_array_of_samples()
    samples_len = len(samples)
    timestep = 1.0/float(mono_first_100_second.frame_rate)
    freqstep = sample_rate/samples_len
    
    # Computer FFT
    fft_real_result = np.fft.fft(samples)
    fft_freq = np.fft.fftfreq(samples_len, d=timestep)
    fft_real_normed = np.abs(fft_real_result) / len(fft_real_result)

    # Find the tuning freqency
    max_sum=0
    max_freq=0
    for frequency in np.arange(424.0, 448.1, 0.10):
        tone=tones[str(frequency)]
        sum=0
        for freq in tone:
            index = int(freq/freqstep)
            sum+=fft_real_normed[index]
        if sum > max_sum:
            max_sum=sum
            max_freq=frequency

    return max_freq

def LoadFolder():
    folder_selected=filedialog.askdirectory()
    types = (   os.path.join(folder_selected, '*.m4a'),
                os.path.join(folder_selected, '*.flac'),
                os.path.join(folder_selected, '*.mp3'), 
                os.path.join(folder_selected, '*.wav'),
                os.path.join(folder_selected, '*.wma'),
                os.path.join(folder_selected, '*.aac')
            ) 
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(files))
    TreeviewFilename_List = []
    for index, Filename in enumerate(Filename_List):
        if Deleted_List[index] == False:
            TreeviewFilename_List.append(Filename)
    for Filename in files_grabbed:
        #print(Filename)
        Filename=Filename.replace("\\", "/")
        if Filename in TreeviewFilename_List:
            continue
        Sampling_Rate=""
        Bitrate=""
        Tone=""
        Status=""
        Deleted=False
        Analyzed=False
        Converted=False
        
        Filename_List.append(Filename)
        Sampling_Rate_List.append(Sampling_Rate)
        Bitrate_List.append(Bitrate)
        Tone_List.append(Tone)
        Status_List.append(Status)
        Deleted_List.append(Deleted)
        Analyzed_List.append(Analyzed)
        Converted_List.append(Converted)
        
        global IndexCounts
        FilesTreeview.insert('', tk.END, values=(IndexCounts, Filename, Sampling_Rate, Bitrate, Tone, Status))
        IndexCounts+=1

def LoadFiles():
    files_selected=filedialog.askopenfilenames(filetypes=[("Audio files", ".m4a .flac .mp3 .wav .wma .aac")])
    TreeviewFilename_List = []
    for index, Filename in enumerate(Filename_List):
        if Deleted_List[index] == False:
            TreeviewFilename_List.append(Filename)
    for Filename in files_selected:
        #print(Filename)
        Filename=Filename.replace("\\", "/")
        if Filename in TreeviewFilename_List:
            continue
        Sampling_Rate=""
        Bitrate=""
        Tone=""
        Status=""
        Deleted=False
        Analyzed=False
        Converted=False
        
        Filename_List.append(Filename)
        Sampling_Rate_List.append(Sampling_Rate)
        Bitrate_List.append(Bitrate)
        Tone_List.append(Tone)
        Status_List.append(Status)
        Deleted_List.append(Deleted)
        Analyzed_List.append(Analyzed)
        Converted_List.append(Converted)
        
        global IndexCounts
        FilesTreeview.insert('', tk.END, values=(IndexCounts, Filename, Sampling_Rate, Bitrate, Tone, Status))
        IndexCounts+=1

def RemoveItems():
    selected_items = FilesTreeview.selection()
    for selected_item in selected_items:
        index=FilesTreeview.set(selected_item, column="id")
        index=int(index)
        Deleted_List[index]=True
        FilesTreeview.delete(selected_item)

def Analyze(selected_item):
    index=FilesTreeview.set(selected_item, column="id")
    index=int(index)
    if not Analyzed_List[index]:
        Filename=Filename_List[index]
        
        song=AudioSegment.from_file(Filename)
        Bitrate=mediainfo(Filename)['bit_rate']
        Bitrate_List[index]=Bitrate
        Sampling_Rate = song.frame_rate
        Sampling_Rate_List[index]=Sampling_Rate
        BitrateStr=str(int(int(Bitrate)/1000))+"kbps"
        Tone=""
        ToneStr=""
        
        Status="Analyzing"
        FilesTreeview.item(selected_item, values=(index, Filename, Sampling_Rate, BitrateStr, ToneStr, Status))
        #root.update_idletasks()
        
        Tone=analyze_tone(song)
        Tone_List[index]=Tone
        ToneStr='%.1f' % Tone + "Hz"
        
        Status="Analyzed"
        FilesTreeview.item(selected_item, values=(index, Filename, Sampling_Rate, BitrateStr, ToneStr, Status))
        #root.update_idletasks()
        
        Analyzed_List[index]=True

def Convert(selected_item):
    index=FilesTreeview.set(selected_item, column="id")
    index=int(index)
    if not Analyzed_List[index]:
        Analyze(selected_item)
    if not Converted_List[index]:
        Filename=Filename_List[index]
        
        TargetBitrate=BitrateComboBox.get()
        TargetSamplingRate=SamplingRateComboBox.get()
        TargetFormat=FormatComboBox.get()
        
        head_tail = os.path.split(Filename)
        folder=head_tail[0]
        filename=head_tail[1]
        extension=filename.split('.')[-1]
        
        if TargetFormat == "Same":
            TargetFormat=extension
            if extension == "aac":
                TargetFormat = "mp3"
            elif extension == "m4a":
                TargetFormat = "mp3"
            elif extension == "wma":
                TargetFormat = "mp3"
            new_filename=os.path.splitext(filename)[0]+'.'+TargetFormat
        else:
            new_filename=os.path.splitext(filename)[0]+'.'+TargetFormat
        
        new_Filename=folder+"/"+"432hz_"+new_filename
        print(Filename, end =" ")
        
        Sampling_Rate=Sampling_Rate_List[index]
        Bitrate=Bitrate_List[index]
        
        Tone=Tone_List[index]
        ToneStr='%.1f' % Tone + "Hz"
        Status="Skipped"
        
        if TargetSamplingRate == "Same":
            TargetSamplingRate = int(Sampling_Rate)
        else:
            TargetSamplingRate = int(TargetSamplingRate)
        
        if TargetBitrate == "Same":
            TargetBitrate=int(Bitrate)
        elif TargetBitrate == "64kbps":
            TargetBitrate=64000
        elif TargetBitrate == "128kbps":
            TargetBitrate=128000
        elif TargetBitrate == "256kbps":
            TargetBitrate=256000
        elif TargetBitrate == "320kbps":
            TargetBitrate=320000
        
        BitrateStr=str(int(int(Bitrate)/1000))+"kbps"
        
        #root.update_idletasks()
        
        # Skip the file which is 432hz or 432hz file is already exisit
        if "432hz_" in filename:
            print("is already a 432hz file, skip...")
            print("")
            FilesTreeview.item(selected_item, values=(index, Filename, Sampling_Rate, BitrateStr, ToneStr, Status))
            #root.update_idletasks()
            return
        
        if os.path.isfile(new_Filename):
            print("is already convert to 432hz, skip...")
            print("")
            FilesTreeview.item(selected_item, values=(index, Filename, Sampling_Rate, BitrateStr, ToneStr, Status))
            #root.update_idletasks()
            return
        
        Status="Converting"
        FilesTreeview.item(selected_item, values=(index, Filename, Sampling_Rate, BitrateStr, ToneStr, Status))
        
        song = AudioSegment.from_file(Filename)
        original_bitrate = mediainfo(Filename)['bit_rate']
        duration = song.duration_seconds
        sample_rate = song.frame_rate
        sample_width = song.sample_width
        channels = song.channels
        
        max_freq=Tone

        # Calculate the 432Hz speed ratio
        print("is",max_freq,"Hz")
        speed_ratio = 432.0/max_freq
        print("Use Speed Ratio",speed_ratio,"to convert...")
        
        # Convert audio
        new_song = speed_change(song, speed_ratio, TargetSamplingRate)
        
        # Save audio
        print("Save to",new_Filename)
        #print("TargetFormat", TargetFormat)
        #print("TargetBitrate", TargetBitrate)
        #new_song.export(new_Filename, format=TargetFormat, bitrate=TargetBitrate)
        new_song.export(new_Filename, format=TargetFormat, bitrate=str(TargetBitrate))
        
        Status="Converted"
        FilesTreeview.item(selected_item, values=(index, Filename, Sampling_Rate, BitrateStr, ToneStr, Status))
        
        Converted_List[index]=True

def ConvertSelectedWorker():
    global thread_ConvertSelected
    thread_ConvertSelected = threading.Thread(target = ConvertSelected)
    thread_ConvertSelected.start()

def ConvertSelected():
    StopButton['state'] = NORMAL
    LoadFolderButton['state'] = DISABLED
    AnalyzeAllButton['state'] = DISABLED
    ConvertAllButton['state'] = DISABLED
    LoadFilesButton['state'] = DISABLED
    AnalyzeButton['state'] = DISABLED
    ConvertButton['state'] = DISABLED
    RemoveItemsButton['state'] = DISABLED
    selected_items = FilesTreeview.selection()
    for selected_item in selected_items:
        global Stop_Flag
        if Stop_Flag:
            print("Stop Flag Detected")
            break
        Convert(selected_item)
    Stop_Flag=False
    StopButton['state'] = DISABLED
    LoadFolderButton['state'] = NORMAL
    AnalyzeAllButton['state'] = NORMAL
    ConvertAllButton['state'] = NORMAL
    LoadFilesButton['state'] = NORMAL
    AnalyzeButton['state'] = NORMAL
    ConvertButton['state'] = NORMAL
    RemoveItemsButton['state'] = NORMAL

def ConvertAllWorker():
    global thread_ConvertAll
    thread_ConvertAll = threading.Thread(target = ConvertAll)
    thread_ConvertAll.start()

def ConvertAll():
    StopButton['state'] = NORMAL
    LoadFolderButton['state'] = DISABLED
    AnalyzeAllButton['state'] = DISABLED
    ConvertAllButton['state'] = DISABLED
    LoadFilesButton['state'] = DISABLED
    AnalyzeButton['state'] = DISABLED
    ConvertButton['state'] = DISABLED
    RemoveItemsButton['state'] = DISABLED
    selected_items = FilesTreeview.get_children()
    for selected_item in selected_items:
        global Stop_Flag
        if Stop_Flag:
            print("Stop Flag Detected")
            break
        Convert(selected_item)
    Stop_Flag=False
    StopButton['state'] = DISABLED
    LoadFolderButton['state'] = NORMAL
    AnalyzeAllButton['state'] = NORMAL
    ConvertAllButton['state'] = NORMAL
    LoadFilesButton['state'] = NORMAL
    AnalyzeButton['state'] = NORMAL
    ConvertButton['state'] = NORMAL
    RemoveItemsButton['state'] = NORMAL


def AnalyzeSelectedWorker():
    global thread_AnalyzeSelected
    thread_AnalyzeSelected = threading.Thread(target = AnalyzeSelected)
    thread_AnalyzeSelected.start()

def AnalyzeSelected():
    StopButton['state'] = NORMAL
    LoadFolderButton['state'] = DISABLED
    AnalyzeAllButton['state'] = DISABLED
    ConvertAllButton['state'] = DISABLED
    LoadFilesButton['state'] = DISABLED
    AnalyzeButton['state'] = DISABLED
    ConvertButton['state'] = DISABLED
    RemoveItemsButton['state'] = DISABLED
    selected_items = FilesTreeview.selection()
    for selected_item in selected_items:
        global Stop_Flag
        if Stop_Flag:
            print("Stop Flag Detected")
            break
        Analyze(selected_item)
    Stop_Flag=False
    StopButton['state'] = DISABLED
    LoadFolderButton['state'] = NORMAL
    AnalyzeAllButton['state'] = NORMAL
    ConvertAllButton['state'] = NORMAL
    LoadFilesButton['state'] = NORMAL
    AnalyzeButton['state'] = NORMAL
    ConvertButton['state'] = NORMAL
    RemoveItemsButton['state'] = NORMAL

def AnalyzeAllWorker():
    global thread_AnalyzeAll
    thread_AnalyzeAll = threading.Thread(target = AnalyzeAll)
    thread_AnalyzeAll.start()

def AnalyzeAll():
    StopButton['state'] = NORMAL
    LoadFolderButton['state'] = DISABLED
    AnalyzeAllButton['state'] = DISABLED
    ConvertAllButton['state'] = DISABLED
    LoadFilesButton['state'] = DISABLED
    AnalyzeButton['state'] = DISABLED
    ConvertButton['state'] = DISABLED
    RemoveItemsButton['state'] = DISABLED
    
    selected_items = FilesTreeview.get_children()
    for selected_item in selected_items:
        global Stop_Flag
        if Stop_Flag:
            print("Stop Flag Detected")
            break
        Analyze(selected_item)
    Stop_Flag=False
    StopButton['state'] = DISABLED
    LoadFolderButton['state'] = NORMAL
    AnalyzeAllButton['state'] = NORMAL
    ConvertAllButton['state'] = NORMAL
    LoadFilesButton['state'] = NORMAL
    AnalyzeButton['state'] = NORMAL
    ConvertButton['state'] = NORMAL
    RemoveItemsButton['state'] = NORMAL

def Stop():
    global Stop_Flag
    Stop_Flag=True

IndexCounts = 0
Index_List = []
Filename_List = []
Sampling_Rate_List = []
Bitrate_List = []
Tone_List = []
Status_List = []
Deleted_List = []
Analyzed_List = []
Converted_List = []
Stop_Flag=False

# Select the folder
root = tk.Tk()
root.title('Exact 432Hz Converter v1.2')
root.geometry('900x500')
#root.filename = filedialog.askdirectory()
#folder_selected = root.filename

root.resizable(0,0)

LoadFolderButton=tk.Button(root, text="Load Folder", height = 2, width = 20, command=LoadFolder)
LoadFolderButton.grid(row=0,column=0,padx=10,pady=10)

AnalyzeAllButton=tk.Button(root, text="Analyze All", height = 2, width = 20, command=AnalyzeAllWorker)
AnalyzeAllButton.grid(row=0,column=1,padx=10,pady=10)

ConvertAllButton=tk.Button(root, text="Convert All", height = 2, width = 20, command=ConvertAllWorker)
ConvertAllButton.grid(row=0,column=2,padx=10,pady=10)

StopButton=tk.Button(root, text="Stop", height = 2, width = 20, command=Stop)
StopButton.grid(row=0,column=3,padx=10,pady=10)
StopButton['state'] = DISABLED

LoadFilesButton=tk.Button(root, text="Load Files", height = 2, width = 20, command=LoadFiles)
LoadFilesButton.grid(row=1,column=0,padx=10,pady=10)

AnalyzeButton=tk.Button(root, text="Analyze Selected", height = 2, width = 20, command=AnalyzeSelectedWorker)
AnalyzeButton.grid(row=1,column=1,padx=10,pady=10)

ConvertButton=tk.Button(root, text="Convert Selected", height = 2, width = 20, command=ConvertSelectedWorker)
ConvertButton.grid(row=1,column=2,padx=10,pady=10)

RemoveItemsButton=tk.Button(root, text="Remove Items", height = 2, width = 20, command=RemoveItems)
RemoveItemsButton.grid(row=1,column=3,padx=10,pady=10)

SamplingRateLabel = tk.Label(root, text='Output Sampling Rate')
SamplingRateLabel.grid(row=2,column=0,padx=10,pady=0)

BitrateLabel = tk.Label(root, text='Output Bitrate')
BitrateLabel.grid(row=2,column=1,padx=10,pady=0)

ToneLabel = tk.Label(root, text='TargetTone')
ToneLabel.grid(row=2,column=2,padx=10,pady=0)

FormatLabel = tk.Label(root, text='Output Format')
FormatLabel.grid(row=2,column=3,padx=10,pady=0)

SamplingRateComboBox = ttk.Combobox(root, values=["Same", "44100", "48000", "96000", "192000"])
SamplingRateComboBox.current(0)
SamplingRateComboBox.grid(row=3,column=0,padx=10,pady=0)

BitrateComboBox = ttk.Combobox(root, values=["Same", "64kbps", "128kbps", "192kbps", "256kbps", "320kbps"])
BitrateComboBox.current(0)
BitrateComboBox.grid(row=3,column=1,padx=10,pady=0)

ToneComboBox = ttk.Combobox(root, values=["432Hz"])
ToneComboBox.current(0)
ToneComboBox.grid(row=3,column=2,padx=10,pady=0)

FormatComboBox = ttk.Combobox(root, values=["Same", "flac", "mp3", "wav"])
FormatComboBox.current(0)
FormatComboBox.grid(row=3,column=3,padx=10,pady=0)

columns = ('id', 'filename', 'sampling_rate', 'bitrate', 'tone', 'status')
FilesTreeview = ttk.Treeview(root, columns=columns, show='headings',height=14)
FilesTreeview.heading('id', text='ID')
FilesTreeview.column('id',width=30,anchor='w',stretch=NO)
FilesTreeview.heading('filename', text='Filename')
FilesTreeview.column('filename',width=480,anchor='w',stretch=NO)
FilesTreeview.heading('sampling_rate', text='SamplingRate')
FilesTreeview.column('sampling_rate',width=100,anchor='w',stretch=NO)
FilesTreeview.heading('bitrate', text='Bitrate')
FilesTreeview.column('bitrate',width=80,anchor='w',stretch=NO)
FilesTreeview.heading('tone', text='Tone')
FilesTreeview.column('tone',width=80,anchor='w',stretch=NO)
FilesTreeview.heading('status', text='Status')
FilesTreeview.column('status',width=100,anchor='w',stretch=NO)
FilesTreeview.grid(row=4,column=0,columnspan=4,padx=0,pady=10)

FileTreeviewVerticalScrlbar = ttk.Scrollbar(root, orient ="vertical", command = FilesTreeview.yview)
FileTreeviewVerticalScrlbar.grid(row=4,column=5,padx=0,pady=10,sticky="nsew")
FilesTreeview.configure(yscrollcommand=FileTreeviewVerticalScrlbar.set)

#for i in range(20):
#    FilesTreeview.insert('', tk.END, values=("test.mp3", "48000", "320kbps", "440.1Hz", "Processing"))

#root.destroy()
root.mainloop()

'''
# Grab supported audio file
types = (os.path.join(folder_selected, '*.mp3'), os.path.join(folder_selected, '*.m4a')) 
files_grabbed = []
for files in types:
    files_grabbed.extend(glob.glob(files))

#Loop for each file
for Filename in files_grabbed:
    # Filename string processing
    Filename=Filename.replace("\\","/")
    head_tail = os.path.split(Filename)
    folder=head_tail[0]
    filename=head_tail[1]
    extension=filename.split('.')[-1]
    new_filename=os.path.splitext(filename)[0]+'.mp3'
    new_Filename=folder+"/"+"432hz_"+new_filename
    print(Filename, end =" ")
    
    # Skip the file which is 432hz or 432hz file is already exisit
    if "432hz_" in filename:
        print("is already a 432hz file, skip...")
        print("")
        continue
    
    if os.path.isfile(new_Filename):
        print("is already convert to 432hz, skip...")
        print("")
        continue
    
    # Read song by Filename and get parameter
    song = AudioSegment.from_file(Filename)
    original_bitrate = mediainfo(Filename)['bit_rate']
    duration = song.duration_seconds
    sample_rate = song.frame_rate
    sample_width = song.sample_width
    channels = song.channels

    max_freq=analyze_tone(song)

    # Calculate the 432Hz speed ratio
    print("is",max_freq,"Hz")
    speed_ratio = 432.0/max_freq
    print("Use Speed Ratio",speed_ratio,"to convert...")
    
    # Convert audio
    new_song = speed_change(song, speed_ratio)
    
    # Save audio
    print("Save to",new_Filename)
    new_song.export(new_Filename, format="mp3", bitrate=original_bitrate)
    
    print("")

os.system("pause")
'''
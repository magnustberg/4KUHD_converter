#Developed by Magnus Berg, 2025 for the University of Toronto, Mississauga Digital Scholarship Unit#
#Are you telling me a TRANS coded this film?

import os
import FreeSimpleGUI as sg
import subprocess
import shutil
import time
import pdb
import ffmpeg
import threading
import multiprocessing
import sys
import cv2
from decimal import Decimal
from pathlib import Path

sg.theme('Reddit')

#Sets what the GUI will look like/have as inputs 
layout = [[sg.Text('4K Upscale Video Converter', font=("bold", 20))],
	[sg.Text('Select the directory that contains the video files', size=(40, 1)), sg.Input(key='-input_dir-'), sg.FolderBrowse()],
	[sg.Text('Select the directory you want to export the files to', size=(40, 1)), sg.Input(key='-output_dir-'), sg.FolderBrowse()],
		[sg.Submit(), sg.Cancel(), sg.Button('Reset', key='-reset-'), sg.Button('Instructions', key='-help-')], 
	[sg.Multiline(size=(100, 5), key='-multiline-', autoscroll=True, visible=True, expand_y=True)],
	[sg.ProgressBar(100, orientation='h', expand_x=True, size=(3, 20),  key='-PBAR-', visible=False)]]
	

window = sg.Window('4K Upscale Video Converter', layout, resizable=True).Finalize()
progress_bar = window.find_element('-PBAR-')
reset = window.find_element('-reset-')


def input_check(input_dir, output_dir):	
#Checks that the user supplied all files, an output directory and filename
	if input_dir and output_dir:
		dir_present = True

#Checks to see if a video stream, two audio streams, filename, and output directory are present. If they are not, alerts the user to add them and try again.
	elif bool(input_dir) == False:
		dir_present = False

	elif bool(output_dir) == False:
		dir_present = False
		
	return dir_present


def dir_safetyCheck(input_dir, output_dir):
#checks that the input and output directory are not the same directory
	if os.stat(input_dir) == os.stat(output_dir):
		dir_safety = False
	else:
		dir_safety = True

	return dir_safety

def dir_emptyCheck(input_dir):
#checks that the input directory is not empty
	if len(os.listdir(input_dir)) == 0:
			dir_empty = True
			
	else:
			dir_empty = False

	return dir_empty

def output_fullCheck(output_dir):
#checks that the output directory is empty
	if len(os.listdir(output_dir)) == 0:
			dir_full = False
	else:
			dir_full = True

	return dir_full
	

def upscale(input_dir, output_dir, file_number):
#performs the upscale operation
	status_number = 0
	try:
		for filename in os.listdir(input_dir):
			input = os.path.join(input_dir, filename)
			if os.path.isfile(input):
					output_prep = Path(filename).stem
					output = os.path.join(output_dir, output_prep)
					ratio_prep = cv2.VideoCapture(input)
					height = ratio_prep.get(cv2.CAP_PROP_FRAME_HEIGHT)
					width = ratio_prep.get(cv2.CAP_PROP_FRAME_WIDTH)
					ratio_prep = Decimal(width/height)
					aspect_ratio = str(round(ratio_prep,2))

					if aspect_ratio=='0.54':
						target_aspectRatio = '1215x2160'
						target = True
					elif aspect_ratio=='0.67':
						target_aspectRatio = '1440x2160'
						target = True
					elif aspect_ratio=='0.80':
						target_aspectRatio = '1728x2160'
						target = True
					elif aspect_ratio=='1.00':
						target_aspectRatio = '2160x2160'
						target = True
					elif aspect_ratio=='1.25':
						target_aspectRatio = '2700x2160'
						target = True
					elif aspect_ratio=='1.33':
						target_aspectRatio = '2880x2160'
						target = True
					elif aspect_ratio=='1.50':
						target_aspectRatio = '3240x2160'
						target = True
					elif aspect_ratio=='1.67':
						target_aspectRatio = '3600x2160'
						target = True
					elif aspect_ratio=='1.78':
						target_aspectRatio = '3840x2160'
						target = True
					elif aspect_ratio=='1.85':
						target_aspectRatio = '3840x2076'
						target = True
					elif aspect_ratio=='1.90':
						target_aspectRatio = '3840x2021'
						target = True
					elif aspect_ratio=='2.00':
						target_aspectRatio = '3840x1920'
						target = True
					elif aspect_ratio=='2.35':
						target_aspectRatio = '3840x1634'
						target = True
					elif aspect_ratio=='2.37':
						target_aspectRatio = '3840x1620'
						target = True
					elif aspect_ratio=='2.39':
						target_aspectRatio = '3840x1600'
						target = True
					elif aspect_ratio=='2.40':
						target_aspectRatio = '3840x1600'
						target = True
					elif aspect_ratio=='2.44':
						target_aspectRatio = '3840x1574'
						target = True
					elif aspect_ratio=='3.00':
						target_aspectRatio = '3840x1280'
						target = True
					elif aspect_ratio=='4.00':
						target_aspectRatio = '3840x960'
						target = True
					else: 
						window['-multiline-'].update('Aspect ratio for ' + output_prep +' is non-standard. Upscale ratio has been inferred. Double check output. \n', append=True)
						target = False

					if target == True:
						command_str = r'ffmpeg -i "' + str(input) + '" -vf "scale=' + target_aspectRatio + ':flags=lanczos" -c:v libx264 -crf 13 -c:a aac -b:a 512k -preset slow "' + str(output) +'.mp4"'
						subprocess.run(command_str, shell=True, stdout=subprocess.PIPE, stderr = subprocess.PIPE, check=True)
					elif target == False:
						command_str = r'ffmpeg -i "' + str(input) + '" -vf "scale=w=3840:h=2160:sws_flags=lanczos:force_original_aspect_ratio=decrease:force_divisible_by=2" -c:v libx264 -crf 13 -c:a aac -b:a 512k -preset slow "' + str(output) +'.mp4"'
						subprocess.run(command_str, shell=True, stdout=subprocess.PIPE, stderr = subprocess.PIPE, check=True)
					
					window['-multiline-'].update(output_prep+' complete'+'\n'+'\n', append=True)
					status_number = status_number + 1
					progress_bar.UpdateBar(status_number, file_number)
						
	except:
		processComplete=True
	else:
		processComplete=False
	
	return processComplete
	
def the_gui():
	open = False
	while True:
		event, values = window.read()

		if event == '-help-':
			window['-multiline-'].update('This application upscales any video file to 4K UHD. Use the browse buttons to select an input and output folder. Any videos in the input folder will be converted, one after another. If there is an error converting one of the files, the progress bar will go red and the application will stop converting the remaining files. Any video files converted before this are fine. Videos with standard aspect ratios will be upscaled to their equivalent in 4K UHD. Video files with a non-standard aspect ratio will have their aspect ratio forced during the upscale process. Double check the output to ensure that there are no issues with the aspect ratio. Once the progress bar is full and the application lets you know the process is done you can close the window. Do not close the window before this as it can halt the conversion process.'+'\n'+'\n', append=True)
	
				
		if event == 'Submit':
			input_dir = values['-input_dir-']
			output_dir = values['-output_dir-']

			input_check_status = input_check(input_dir, output_dir)

			if input_check_status == False:
				window['-multiline-'].update('All fields must be complete in order to continue. Please try again.'+'\n'+'\n', append=True)
				check_status=False
			else:
				safety_check_status = dir_safetyCheck(input_dir, output_dir)
			
				if safety_check_status == False:
					window['-multiline-'].update('The input and output directories cannot be the same. Please try again.'+'\n'+'\n', append=True)
					check_status=False
			
				else:
					empty_check_status = dir_emptyCheck(input_dir)
				
					if empty_check_status == True:
						window['-multiline-'].update('The input directory is empty, there are no files to process. Please try again.'+'\n'+'\n', append=True)
						check_status = False

					else:
						full_check=output_fullCheck(output_dir)

						if full_check == True:
							window['-multiline-'].update('The output directory has files present. Please use an empty directory to avoid overwriting files.'+'\n'+'\n', append=True)
							check_status = False	

						elif full_check == False:
							check_status = True

			if check_status == True:
				
				window['-multiline-'].update('Files added to queue. Please wait. DO NOT close this window.'+'\n'+'\n', append=True)
			
				file_list = os.listdir(input_dir)
				file_number = len(file_list)
			
				progress_bar.update(visible=True)
				progress_bar.UpdateBar(0, file_number)


				window.perform_long_operation(lambda: upscale(input_dir, output_dir, file_number), '-Process Complete-')
			
		elif event == '-Process Complete-':
			process_status = {values[event]}
			if process_status=={0}:
				window.write_event_value('-failure-', False)
			else:
				window.write_event_value('-failure-', True)
		
		elif event == '-failure-':
			failure=values['-failure-']
			if failure==True:
				window['-multiline-'].update('One or more processes have failed. Unable to continue.'+'\n'+'\n', append=True)
				progress_bar.update(bar_color=('red'))

			else:
				window['-multiline-'].update('Processing complete. You can now close the window.'+'\n'+'\n', append=True)

		elif event == '-reset-':
			progress_bar.update(visible=False)
			window['-multiline-'].update('')
			window.find_element('-input_dir-').update('')
			window.find_element('-output_dir-').update('')

		elif event == sg.WIN_CLOSED or event == 'Cancel':
			break
			window.close()

if __name__=='__main__':
	the_gui()
				
					
	
		
	
	

#Download “release full” build. It will have the largest set of libraries with greater functionality. For example full build https://github.com/GyanD/codexffmpeg/releases/tag/2022-12-15-git-9adf02247c
#Extract the contents in the ZIP file to a folder of your choice.
#To add FFmpeg to Win10 path. (User variables -> Path -> New and add)
#Verify. Open the Command Prompt or PowerShell window, type FFmpeg, and press Enter.

import m3u8_To_MP4
import os
import subprocess

def temp_folder_cleaner(temp_segments):
    # remove all files from temp_segments directory for clean start
    for file in os.listdir(temp_segments):
        os.remove(os.path.join(temp_segments, file))


def download_stream_to_mp4(url, mp4_file_dir, temp_segments):
    # remove evertyhing after ? charachter
    url = url.split('?')[0]
    # get final file name from url 
    mp4_file_name = url.split('/')[-3]
    full_mp4_file_name = f'{mp4_file_name}.mp4'
    # remove all files from temp_segments directory for clean start
    temp_folder_cleaner(temp_segments)
    
    print('============================================================================================')
    print(f'Final URL: {url}')
    print(f'Final file is in directory: {mp4_file_dir}')
    print(f'Final file name: {full_mp4_file_name}')
    
    if  full_mp4_file_name in os.listdir(mp4_file_dir):
        print(f'File {full_mp4_file_name} already exists in {mp4_file_dir}')
    else:
        print(f'Final file NOT IN: {full_mp4_file_name} and will be downloaded')
        print('============================================================================================')

    # loop untill same item full_mp4_file_name is not in mp3_file_dir
    while full_mp4_file_name not in os.listdir(mp4_file_dir):
        # Download videos from uri and save to mp4_file_dir
        m3u8_To_MP4.multithread_download(m3u8_uri=url, mp4_file_dir=mp4_file_dir, tmpdir=temp_segments, mp4_file_name=mp4_file_name, max_retry_times=10, max_num_workers=200)
        # detele all file from temp_segments to clean up used files
        temp_folder_cleaner(temp_segments)


if __name__ == '__main__':
    
    # set variables
    temp_segments = 'temp'
    mp4_file_dir = 'Luise ja Oliver'
    links_txt_file = 'Luise ja Oliver m3u8 links.txt'

    # create temp_segments and mp4_file_dir folders if not exists
    if not os.path.exists(temp_segments):
        os.mkdir(temp_segments)
    if not os.path.exists(mp4_file_dir):
        os.mkdir(mp4_file_dir)
    
    # get full path to temp_segments and mp4_file_dir folder
    temp_segments = os.path.abspath(temp_segments)
    mp4_file_dir = os.path.abspath(mp4_file_dir)
    
    # Run the 'ffmpeg' PowerShell command
    result = subprocess.run(['powershell.exe', 'ffmpeg'], stdout=subprocess.PIPE).stdout.decode()
    if 'ObjectNotFound:' in result:
        print('FFmpeg not found. Please install it and add to env path')
        exit(1)
    else:
        # read in m3u8 links from file
        for url in open(links_txt_file, 'r'):
            download_stream_to_mp4(url=url, mp4_file_dir=mp4_file_dir, temp_segments=temp_segments)
    print('============================================================================================')
    print('All files downloaded')

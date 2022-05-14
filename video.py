# import subprocess in case this cell is run without the above cells
import subprocess
import torch
import sys
import os
import re
from tqdm import tqdm
from PIL import Image

# Try to avoid OOM errors
torch.cuda.empty_cache()

# cwd = os.getcwd()
# output = "output.mp4"

# filepath = f'{cwd}/{output}'

# frames = []
# tqdm.write('Generating video...')
# image_path = f'{cwd}/VQGAN-CLIP/steps/zoomed_*.png'

# cmd = [
#     'ffmpeg',
#     '-y',
#     '-vcodec',
#     'png',
#     '-r',
#     str(fps),
#     '-start_number',
#     str(init_frame),
#     '-pattern_type '
#     'glob',
#     '-i',
#     image_path,
#     '-c:v',
#     'libx264',
#     '-frames:v',
#     str(last_frame-init_frame),
#     '-vf',
#     f'fps={fps}',
#     '-pix_fmt',
#     'yuv420p',
#     '-crf',
#     '17',
#     '-preset',
#     'veryslow',
#     filepath
# ]

# process = subprocess.Popen(cmd, cwd=f'{cwd}/VQGAN-CLIP/steps/', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# stdout, stderr = process.communicate()
# if process.returncode != 0:
#     print(stderr)
#     print(
#         "You may be able to avoid this error by backing up the frames,"
#         "restarting the notebook, and running only the google drive/local connection and video synthesis cells,"
#         "or by decreasing the resolution of the image generation steps. "
#         "If these steps do not work, please post the traceback in the github."
#     )
#     raise RuntimeError(stderr)
# else:
#     print("The video is ready")
import argparse

parser = argparse.ArgumentParser(description='SRCNN run parameters')
parser.add_argument('-if', '--init_frame', type=int, required=True)
parser.add_argument('-lf', '--last_frame', type=int, required=True)
parser.add_argument('-sp', '--scaled_path', type=str, required=True, help="like '/scaled_frames/dada'")
parser.add_argument('-op', '--out_path', type=str, required=True, help="like '/output/dada.mp4'")
parser.add_argument('-fps', '--fps', type=int, required=True)
args = parser.parse_args()


def run_stitch(init_frame, last_frame, fps, in_file_template, out_file_path):
    frames = []
    for i in range(init_frame,last_frame):
        temp = Image.open(in_file_template.format(i))
        keep = temp.copy()
        frames.append(keep)
        temp.close()
        if i % 200 == 0:
            print(i)
    ffmpeg_filter = f"minterpolate='mi_mode=mci:me=hexbs:me_mode=bidir:mc_mode=aobmc:vsbmc=1:mb_size=8:search_param=32:fps={fps}'"
    tqdm.write('Generating video...')
    # output_file = re.compile('\.png$').sub('.mp4', "output.mp4")
    try:
        p = subprocess.Popen(['/usr/bin/ffmpeg',
                '-y',
                '-f', 'image2pipe',
                '-vcodec', 'png',
                '-r', str(fps),               
                '-i',
                '-',
                '-vcodec', 'libx264',
                '-r', str(fps),               
                '-pix_fmt', 'yuv420p',
                '-crf', '17',
                '-preset', 'veryslow',
                # '-strict', 'experimental',
            out_file_path], stdin=subprocess.PIPE)
        # GPU (pytorch docker didn't have udpated nvidia drivers)
        # p = subprocess.Popen(['/usr/bin/ffmpeg',
        #             '-y',
        #             '-f', 'image2pipe',
        #             '-vcodec', 'png',
        #             '-r', str(fps),               
        #             '-i',
        #             '-',
        #             '-b:v', '10M',
        #             '-vcodec', 'h264_nvenc',
        #             '-pix_fmt', 'yuv420p',
        #             '-strict', '-2',
        #             '-filter:v', f'{ffmpeg_filter}',
        #         out_file_path], stdin=subprocess.PIPE)
    except FileNotFoundError:
        print("ffmpeg command failed - check your installation")
    for im in tqdm(frames):
        im.save(p.stdin, 'PNG')
    p.stdin.close()
    p.wait()

if __name__ == "__main__":
    scaled_path_template = os.getcwd() + args.scaled_path + "/{}.png"
    video_out_file = os.getcwd() + args.out_path
    run_stitch(args.init_frame, args.last_frame+1, args.fps, scaled_path_template, video_out_file)
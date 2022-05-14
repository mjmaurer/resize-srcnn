# import subprocess in case this cell is run without the above cells
import argparse
import subprocess
import os
import sys
import run
import video
# Set zoomed = True if this cell is run
zoomed = True

parser = argparse.ArgumentParser(description='SRCNN run parameters')
parser.add_argument('-if', '--init_frame', type=int, required=True)
parser.add_argument('-lf', '--last_frame', type=int, required=True)
parser.add_argument('-ip', '--input_path', type=str, required=True, help="like '/input_frames/dada'")
parser.add_argument('-sp', '--scaled_path', type=str, required=True, help="like '/scaled_frames/dada'")
parser.add_argument('-op', '--out_path', type=str, required=True, help="like '/output/dada.mp4'")
parser.add_argument('-zf', '--zoom_factor', type=int, required=True)
parser.add_argument('-fps', '--fps', type=int, required=True)
args = parser.parse_args()

if args.input_path == args.scaled_path:
    raise Error("in == scaled path")

for i in range(args.init_frame, args.last_frame + 1): #
    # filename = f"{i}.png"
    # cmd = [
    #     'python',
    #     f'{os.getcwd()}/run.py',
    #     '--zoom_factor',
    #     '2',  # Note if you increase this, you also need to change the model.
    #     '--model',
    #     f'{os.getcwd()}/models/model_2x.pth',
    #     '--image',
    #     filename,
    #     '--cuda'
    # ]
    # print(f'Upscaling frame {i}')
    if i % 25 == 0:
        print(i)
    in_path = f"{os.getcwd()}{args.input_path}/{i}.png"
    out_path = f"{os.getcwd()}{args.scaled_path}/{i}.png"
    run.run_scale(args.zoom_factor, in_path, out_path)

    # process = subprocess.Popen(cmd, cwd=f'{os.getcwd() + steps_path}')
    # stdout, stderr = process.communicate()
    # if process.returncode != 0:
    #     print(stderr)
    #     print(
    #         "You may be able to avoid this error by backing up the frames,"
    #         "restarting the notebook, and running only the video synthesis cells,"
    #         "or by decreasing the resolution of the image generation steps. "
    #         "If you restart the notebook, you will have to define the `filepath` manually"
    #         "by adding `filepath = 'PATH_TO_THE_VIDEO'` to the beginning of this cell. "
    #         "If these steps do not work, please post the traceback in the github."
    #     )
    #     raise RuntimeError(stderru
scaled_path_template = os.getcwd() + args.scaled_path + "/{}.png"
video_out_file = os.getcwd() + args.out_path
video.run_stitch(args.init_frame, args.last_frame, args.fps, scaled_path_template, video_out_file)
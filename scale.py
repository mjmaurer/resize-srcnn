# import subprocess in case this cell is run without the above cells
import subprocess
import os
import sys
# Set zoomed = True if this cell is run
zoomed = True

init_frame = int(sys.argv[1])
last_frame = int(sys.argv[2])

for i in range(init_frame, last_frame + 1): #
    filename = f"{i}.png"
    cmd = [
        'python',
        f'{os.getcwd()}/SRCNN/run.py',
        '--zoom_factor',
        '4',  # Note if you increase this, you also need to change the model.
        '--model',
        f'{os.getcwd()}/SRCNN/models/model_4x.pth',
        '--image',
        filename,
        '--cuda'
    ]
    print(f'Upscaling frame {i}')

    process = subprocess.Popen(cmd, cwd=f'{os.getcwd()}/VQGAN-CLIP/steps')
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(stderr)
        print(
            "You may be able to avoid this error by backing up the frames,"
            "restarting the notebook, and running only the video synthesis cells,"
            "or by decreasing the resolution of the image generation steps. "
            "If you restart the notebook, you will have to define the `filepath` manually"
            "by adding `filepath = 'PATH_TO_THE_VIDEO'` to the beginning of this cell. "
            "If these steps do not work, please post the traceback in the github."
        )
        raise RuntimeError(stderr)

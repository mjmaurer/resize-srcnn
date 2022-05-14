FROM pytorch/pytorch

RUN apt-get update && apt-get install -y ffmpeg

CMD /bin/bash
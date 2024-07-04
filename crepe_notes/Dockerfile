FROM nvidia/cuda:12.5.0-devel-ubuntu22.04
RUN apt update && apt install python3 python3-pip -y
RUN python3 -m pip install tensorflow cython
RUN python3 -m pip install crepe-notes
RUN apt install git -y
RUN python3 -m pip install git+https://github.com/CPJKU/madmom#egg=madmom

#!/bin/bash

## resolve folder of this script, following all symlinks,
## http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
SCRIPT_SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SCRIPT_SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  SCRIPT_DIR="$( cd -P "$( dirname "$SCRIPT_SOURCE" )" && pwd )"
  SCRIPT_SOURCE="$(readlink "$SCRIPT_SOURCE")"
  # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
  [[ $SCRIPT_SOURCE != /* ]] && SCRIPT_SOURCE="$SCRIPT_DIR/$SCRIPT_SOURCE"
done
readonly SCRIPT_DIR="$( cd -P "$( dirname "$SCRIPT_SOURCE" )" && pwd )"
cd "${SCRIPT_DIR}"

if which sudo ; then
  SUDO=sudo
else
  SUDO=
fi

# To tun later container with gui:
# xhost +"local:podman@" #<- normal user !!! mandatory
# GUI_PART="-v /tmp/.X11-unix:/tmp/.X11-unix:ro -e \"DISPLAY\" --security-opt label=type:container_runtime_t "
# podman run $GUI_PART  -e DISPLAY=$DISPLAY  -ti  worstcrosswords  python ...
if [ "x$CONTAINER_BUILD" == "xTrue" ] ; then
  set -e
  podman build --tag worstcrosswords .
  podman save -o WorstCrossWords.tar worstcrosswords
  exit 0
fi

if [ "x$SELF_INIT" == "xTrue" ] ; then
  $SUDO dnf install -y git
  $SUDO useradd game
  $SUDO su game -c "cd ~ && git clone https://github.com/judovana/WorstCrossWords.git && cd ~/WorstCrossWords && git checkout main"
fi

if [ "x$ROOT_INSTALL" == "xTrue" -o  "x$ROOT_INSTALL" == "x" ] ; then
  $SUDO dnf install -y python pip
  $SUDO dnf install -y python-tkinter
fi

if [ ! -e tokenization_small100.py ] ; then
  curl -k -f -L -O https://huggingface.co/alirezamsh/small100/raw/main/tokenization_small100.py
fi


if [ "x$PIP_INSTALL" == "xTrue" -o  "x$PIP_INSTALL" == "x" ] ; then
  pip install diffusers
  pip install torch
  pip install accelerate
  pip install transformers
  pip install sentencepiece
  #pip install python-tk
  pip install pillow
  #pip install tkinter
fi

if [ "x$GEN_MODELS" == "xTrue" -o  "x$GEN_MODELS" == "x" ] ; then
  set -e
  #download the 2/3 models
  python translate.py en koza
  python explain.py  lion
  #check gui
  #python show_image.py  "${BASH_SOURCE[0]}" || echo  'run xhost +"local:podman@" and add "-v /tmp/.X11-unix:/tmp/.X11-unix:ro -e \"DISPLAY\" --security-opt label=type:container_runtime_t -e DISPLAY=$DISPLAY" to your  container run'
  #download the 3/3 models
  NO_SHOW=True python generateImage.py sixtieths
  rm outgen*.jpg
fi



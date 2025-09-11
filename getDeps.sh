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

# To run later container with gui:
# xhost +"local:podman@" #<- normal user !!! mandatory
# GUI_PART="-v /tmp/.X11-unix:/tmp/.X11-unix:ro -e \"DISPLAY\" --security-opt label=type:container_runtime_t "
# podman run $GUI_PART  -e DISPLAY=$DISPLAY  -ti  worstcrosswords  python ...
if [ "x$CONTAINER_BUILD" == "xTrue" ] ; then
  echo "Building containres."
  echo "1: emptyone, where you ahve to mount local cache, as -v=your_local_dir_with_ai_cahe:/home/game/WorstCrossWords/cache"
  echo "eg  -v=./cache:/home/game/WorstCrossWords/cache"
  echo "To run this with gui, you must: "
  echo 'xhost +"local:podman@" #<- normal user !!! mandatory'
  echo 'GUI_PART="-v /tmp/.X11-unix:/tmp/.X11-unix:ro -e \"DISPLAY\" --security-opt label=type:container_runtime_t"'
  echo "eg:"
  echo 'podman run $GUI_PART  -e DISPLAY=$DISPLAY  -v=./cache:/home/game/WorstCrossWords/cache -ti  worstcrosswords_empty python show_image.py getDeps.sh'
  echo "and you should see exempalr gui window. All cmds will do: caches.py explain.py game.py generateImage.py generateWords.py show_image.py show_images.py shuffle.pyt ranslate.py"

  echo "primarily 'game.py' of course"
  rm WorstCrossWords*.tar
  set -e
  podman build --tag worstcrosswords_base .
  echo "FROM worstcrosswords_base
RUN mkdir cache
" > empty
  podman build --file empty --tag worstcrosswords_empty .
  podman save -o WorstCrossWords_empty.tar worstcrosswords_empty
  rm empty
  if [ "$#" -eq 0 ]; then
    echo "No dirs/archives with caches provided, exiting"; 
  else
    echo "buiding image with read-only caches"
    rm -rf cont_build_caches
    mkdir cont_build_caches
    echo "FROM worstcrosswords_base
RUN mkdir cache
" > full
    i=0;
    for arg in "$@"; do
      let i=i+1
      if [ -d $arg -a $arg == "cache" ] ; then
         cp -rv $arg  cont_build_caches/cache$1
      elif [ -d $arg ] ; then
         cp -rv $arg/cache  cont_build_caches/cache$1
      elif [ -f $arg ] ; then
         tar -xvf $arg -C cont_build_caches cache
         mv cache cache$1
      fi
      echo "COPY cont_build_caches/cache$1/* /home/game/WorstCrossWords/cache/" >> full
    done
    podman build --file full --tag worstcrosswords_full .
    podman save -o WorstCrossWords_full.tar worstcrosswords_full
    rm -rf cont_build_caches
    rm full
    echo "this container do not need (and can not have), and contain some caches already as simle (35GB..) demo"
  fi
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



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

if [ ! "x$CONTAINER_BUILD" == "xTrue" ] ; then
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
    pip install torch==2.8.0
    pip install diffusers==0.35.1
    pip install accelerate==1.10.1
    pip install transformers==4.56.2
    pip install sentencepiece==0.2.1
    pip install pillow
  fi
  if [ "x$GEN_MODELS1" == "xTrue" -o  "x$GEN_MODELS1" == "x" ] ; then
    set -e
    #download the 1/3 models
    python translate.py en koza
  fi
  if [ "x$GEN_MODELS2" == "xTrue" -o  "x$GEN_MODELS2" == "x" ] ; then
    set -e
    #download the 2/3 models
    python explain.py  lion
  fi
  if [ "x$GEN_MODELS3" == "xTrue" -o  "x$GEN_MODELS3" == "x" ] ; then
    #check gui
    #python show_image.py  "${BASH_SOURCE[0]}" || echo  'run xhost +"local:podman@" and add "-v /tmp/.X11-unix:/tmp/.X11-unix:ro -e \"DISPLAY\" --security-opt label=type:container_runtime_t -e DISPLAY=$DISPLAY" to your  container run'
    #download the 3/3 models
    NO_SHOW=True python generateImage.py sixtieths
    rm outgen*.jpg
  fi
fi


if [ "x$CONTAINER_BUILD" == "xTrue" ] ; then
  echo "Building containres."
  echo "1. full one. This contain some caches already as simle (35GB..) demo. This container do not need (and should not have the mount (the -v))"
  echo "To run properly this with gui, you must: "
  echo 'xhost +"local:podman@" #<- normal user !!! mandatory'
  echo 'GUI_PART="-v /tmp/.X11-unix:/tmp/.X11-unix:ro -e \"DISPLAY\" --security-opt label=type:container_runtime_t"'
  echo "eg:"
  echo 'podman run $GUI_PART  -e DISPLAY=$DISPLAY  -ti  worstcrosswords_empty python show_image.py getDeps.sh'
  echo "and you should see exempalr gui window. All cmds will do: caches.py explain.py game.py generateImage.py generateWords.py show_image.py show_images.py shuffle.pyt ranslate.py"
  echo "primarily 'game.py' of course"
  rm WorstCrossWords*.tar
  set -e
  podman build --tag worstcrosswords_base . # the in tree Containerfile
  echo "FROM worstcrosswords_base
RUN pwd
RUN ls -R
" > full
  if [ "$#" -eq 0 ]; then
    echo "No dirs/archives with caches tobe mixed inside on cmd line, skipping"; 
  else
    echo "adding custom caches inside"
    CBUILD_DIR=cont_build_caches
    rm -rf ${CBUILD_DIR}
    mkdir ${CBUILD_DIR}
    i=0;
    for arg in "$@"; do
      let i=i+1
      if [ -d $arg -a $arg == "cache" ] ; then
         cp -rv $arg  ${CBUILD_DIR}/cache${i}
         echo "COPY ${CBUILD_DIR}/cache${i}/ /home/game/WorstCrossWords/cache/" >> full
      elif [ -d $arg ] ; then
         cp -rv $arg/cache  ${CBUILD_DIR}/cache${i}
         echo "COPY ${CBUILD_DIR}/cache${i}/ /home/game/WorstCrossWords/cache/" >> full
      elif [ -f $arg ] ; then
         tar -xvf $arg -C ${CBUILD_DIR} cache
         mv -v ${CBUILD_DIR}/cache ${CBUILD_DIR}/cache${i}
         echo "COPY ${CBUILD_DIR}/cache${i}/ /home/game/WorstCrossWords/cache/" >> full
      else
        "unknown cache source $arg. use 'cahce' or 'dir/cache' folders, or tar chvies with dir 'cache'"
      fi
    done
  fi
  podman build --file full --tag worstcrosswords .
  if [ "x$CONTAINER_SAVE" == "xTrue" ] ; then  podman save -o WorstCrossWords.tar worstcrosswords ; fi
  if [ "x$CONTAINER_PUBLISH" == "xTrue" ] ; then echo "podman login quay.io#?email/pass";  podman push worstcrosswords  quay.io/judovana/worstcrosswords ; fi
  rm full
  echo "FROM worstcrosswords_base
RUN pwd
RUN rm -rf cache
RUN mkdir cache
RUN ls -R
" > empty
  podman build --file empty --tag worstcrosswords_empty .
  if [ "x$CONTAINER_SAVE" == "xTrue" ] ; then podman save -o WorstCrossWords_full.tar worstcrosswords_full ; fi
  if [ "x$CONTAINER_PUBLISH" == "xTrue" ] ; then echo "podman login quay.io#?email/pass";  podman push worstcrosswords_full  quay.io/judovana/worstcrosswords ; fi
  rm -rf ${CBUILD_DIR}
  rm empty
  echo "2: emptyone, where you have to mount local cache, as -v=<your_local_dir_with_ai_cahe>:/home/game/WorstCrossWords/cache"
  echo "eg  -v=./cache:/home/game/WorstCrossWords/cache"
  echo " be sure, your <your_custom_cache_dir> have corrrect permissions"
  echo " yo can always run 'chmod -777' on <your_custom_cache_dir> before (and after if you share the cache with local instance) container run"
  echo " you can map the uid/gid of game user in container, but it is quite compelx to do properly"
  echo "To run this with gui, you must: "
  echo 'xhost +"local:podman@" #<- normal user !!! mandatory'
  echo 'GUI_PART="-v /tmp/.X11-unix:/tmp/.X11-unix:ro -e \"DISPLAY\" --security-opt label=type:container_runtime_t"'
  echo 'podman run $GUI_PART  -e DISPLAY=$DISPLAY  -v=./cache:/home/game/WorstCrossWords/cache -ti  worstcrosswords_empty python show_image.py getDeps.sh'
  echo "and you should see exempalr gui window. All cmds will do: caches.py explain.py game.py generateImage.py generateWords.py show_image.py show_images.py shuffle.pyt ranslate.py"
  echo "primarily 'game.py' of course"
  exit 0
fi

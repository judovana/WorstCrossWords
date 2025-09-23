# used by CONTAINER_BUILD=True sh getDeps.sh
FROM fedora:42
RUN dnf install -y sudo /usr/bin/which
RUN curl -k -f -L -O https://raw.githubusercontent.com/judovana/WorstCrossWords/refs/heads/cont3/getDeps.sh
RUN SELF_INIT=True ROOT_INSTALL=False PIP_INSTALL=False GEN_MODELS1=False GEN_MODELS2=False GEN_MODELS3=False sh -ex getDeps.sh
RUN SELF_INIT=False ROOT_INSTALL=True PIP_INSTALL=False GEN_MODELS1=False GEN_MODELS2=False GEN_MODELS3=False sh -ex getDeps.sh
RUN rm getDeps.sh
USER game
WORKDIR /home/game/WorstCrossWords

# diverging from getDeps by isntalling the deps one by one ro create proepr layers acceptable by quay
# reverse enginered from logs:( ; necessar to split giantic layer pip otherwise creates
RUN pip install mpmath==1.3.0
RUN pip install networkx==3.5
RUN pip install sympy==1.14.0
RUN pip install setuptools==80.9.0
RUN pip install triton==3.4.0
RUN pip install nvidia_nvjitlink_cu12==12.8.93
RUN pip install nvidia_nccl_cu12==2.27.3
RUN pip install nvidia_cusparselt_cu12==0.7.1
RUN pip install nvidia_cusparse_cu12==12.5.8.93
RUN pip install nvidia_cusolver_cu12==11.7.3.90
RUN pip install nvidia_curand_cu12==10.3.9.90
RUN pip install nvidia_cufile_cu12==1.13.1.3
RUN pip install nvidia_cufft_cu12==11.3.3.83
RUN pip install nvidia_cudnn_cu12==9.10.2.21
RUN pip install nvidia_cuda_runtime_cu12==12.8.90
RUN pip install nvidia_cuda_nvrtc_cu12==12.8.93
RUN pip install nvidia_cuda_cupti_cu12==12.8.90
RUN pip install nvidia_cublas_cu12==12.8.4.1
RUN pip install torch==2.8.0

#reruning main target just inc ase something was lost
RUN SELF_INIT=False ROOT_INSTALL=False PIP_INSTALL=True GEN_MODELS1=False GEN_MODELS2=False GEN_MODELS3=False sh -ex getDeps.sh

# diverging again in attempt to split giantic model layers
RUN python explain.py  --version
RUN python generateImage.py  --version
RUN python translate.py  --version
RUN python explain.py  --init
RUN python generateImage.py  --init
RUN python translate.py  --init1
RUN python translate.py  --init2

#reruning main targets just inc ase something was lost
RUN SELF_INIT=False ROOT_INSTALL=False PIP_INSTALL=False GEN_MODELS1=True GEN_MODELS2=False GEN_MODELS3=False sh -ex getDeps.sh
RUN SELF_INIT=False ROOT_INSTALL=False PIP_INSTALL=False GEN_MODELS1=False GEN_MODELS2=True GEN_MODELS3=False sh -ex getDeps.sh
RUN SELF_INIT=False ROOT_INSTALL=False PIP_INSTALL=False GEN_MODELS1=False GEN_MODELS2=False GEN_MODELS3=True sh -ex getDeps.sh

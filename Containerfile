FROM fedora:42
RUN dnf install -y sudo /usr/bin/which
RUN curl -k -f -L -O https://raw.githubusercontent.com/judovana/WorstCrossWords/refs/heads/main/getDeps.sh
RUN SELF_INIT=True ROOT_INSTALL=False PIP_INSTALL=False GEN_MODELS1=False GEN_MODELS2=False GEN_MODELS3=False sh -x getDeps.sh
RUN SELF_INIT=False ROOT_INSTALL=True PIP_INSTALL=False GEN_MODELS1=False GEN_MODELS2=False GEN_MODELS3=False sh -x getDeps.sh
RUN rm getDeps.sh
USER game
WORKDIR /home/game/WorstCrossWords
RUN SELF_INIT=False ROOT_INSTALL=False PIP_INSTALL=True GEN_MODELS1=False GEN_MODELS2=False GEN_MODELS3=False sh -x getDeps.sh
RUN SELF_INIT=False ROOT_INSTALL=False PIP_INSTALL=False GEN_MODELS1=True GEN_MODELS2=False GEN_MODELS3=False sh -x getDeps.sh
RUN SELF_INIT=False ROOT_INSTALL=False PIP_INSTALL=False GEN_MODELS1=False GEN_MODELS2=True GEN_MODELS3=False sh -x getDeps.sh
RUN SELF_INIT=False ROOT_INSTALL=False PIP_INSTALL=False GEN_MODELS1=False GEN_MODELS2=False GEN_MODELS3=True sh -x getDeps.sh

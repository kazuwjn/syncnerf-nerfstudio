ARG BASE_IMAGE
FROM ${BASE_IMAGE}

ARG PROJECT_NAME
ARG USER_NAME
ARG GROUP_NAME
ARG UID
ARG GID
ARG APPLICATION_DIRECTORY=/home/${USER_NAME}/${PROJECT_NAME}
ARG ANACONDA_FILE

ENV DEBIAN_FRONTEND="noninteractive" \
    LC_ALL="C.UTF-8" \
    LANG="C.UTF-8"

RUN apt update && apt install --no-install-recommends -y \
    git curl make ssh openssh-client

# Add user. Without this, following process is executed as admin. 
RUN groupadd -g ${GID} ${GROUP_NAME} \
    && useradd -ms /bin/sh -u ${UID} -g ${GID} ${USER_NAME}

RUN apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6 wget -y && \
    wget -P /opt https://repo.anaconda.com/archive/${ANACONDA_FILE} && \
    bash /opt/${ANACONDA_FILE} -b -p /opt/anaconda3 && \
    rm /opt/${ANACONDA_FILE} && \
    echo "export PATH=/opt/anaconda3/bin:$PATH" >> /home/${USER_NAME}/.bashrc && \
    . /home/${USER_NAME}/.bashrc

RUN apt-get install -y libglib2.0-0

USER ${USER_NAME}
WORKDIR ${APPLICATION_DIRECTORY}
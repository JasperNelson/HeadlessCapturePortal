FROM ubuntu:latest
EXPOSE 80
EXPOSE 443
RUN apt install -y firefox gnome-keyring dbus pyenv python
ENV HOME  /home/python_user
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
RUN git clone https://github.com/pyenv/pyenv-update.git $PYENV_ROOT/plugins/pyenv-update
RUN pyenv update 
RUN pyenv install -f 3.12.2 
RUN pyenv global 3.12.2
RUN pyenv rehash
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt 
RUN dbus-run-session -- sh 
RUN echo 'creds' | gnome-keyring-daemon







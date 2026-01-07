FROM python:3.14-bookworm AS base

# 環境変数とタイムゾーンの設定
ENV TZ=Asia/Tokyo
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

# 基本パッケージのインストール
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update && \
    apt-get install -y \
    locales \
    zip \
    unzip \
    vim \
    git \
    keychain \
    curl \
    less && \
    localedef -i ja_JP -c -f UTF-8 -A /usr/share/locale/locale.alias ja_JP.UTF-8

# Python tools インストール
FROM base AS python-tools
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir \
    black \
    flake8 \
    mypy \
    pytest \
    pytest-cov \
    pylint \
    autopep8 \
    isort

# Task Runner インストール
FROM base AS task-runner
RUN --mount=type=cache,target=/tmp/task \
    curl -sL "https://github.com/go-task/task/releases/download/v3.9.0/task_linux_amd64.deb" -o /tmp/task/task.deb && \
    dpkg -i /tmp/task/task.deb

# 最終ステージ
FROM base AS final
ENV APP_ROOT /home/dev/data

# Node.js をインストール
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Serverless Framework をインストール
RUN --mount=type=cache,target=/root/.npm \
    npm install -g serverless@3

# Python toolsをコピー
COPY --from=python-tools /usr/local/bin /usr/local/bin
COPY --from=python-tools /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages

# Task Runnerをコピー
COPY --from=task-runner /usr/local/bin/task /usr/local/bin/task

# SSH keychain設定
RUN eval `keychain --eval --agents ssh id_rsa`

RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh
RUN mkdir -p /home/dev/.codex

# Node.js (v22) インストール
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get update && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Codexを公式ガイド通りにグローバルインストール
RUN npm i -g @openai/codex

RUN mkdir -p $APP_ROOT
# 開発ユーザー作成
RUN groupadd -g 1000 dev && \
    useradd -m -u 1000 -g dev -s /bin/bash dev && \
    chown -R dev:dev /home/dev

# VS Code Server 用ディレクトリ
# VS Code Server 用のディレクトリを事前に作成して権限を設定
RUN mkdir -p /home/dev/.vscode-server/bin /home/dev/.vscode-server/extensions && \
    chown -R dev:dev /home/dev/.vscode-server


WORKDIR $APP_ROOT

USER dev

# bashrcのコピー
COPY --chown=dev:dev .devcontainer/infra/python/.bashrc /home/dev/.bashrc

# Claude Code インストール
RUN curl -fsSL https://claude.ai/install.sh | bash && \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> /home/dev/.bashrc && \
    echo 'eval `keychain --eval --agents ssh id_rsa 2>/dev/null`' >> /home/dev/.bashrc

ENV PATH="/home/dev/.local/bin:${PATH}"
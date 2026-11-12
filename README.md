# プロジェクト概要

本リポジトリは Farm Replace のリポジトリです。  
https://store.steampowered.com/app/2060160/_Replace/

## 使用技術

### 言語

- Python 3.14（Dev Container）

### ローカル環境

- Docker
- DevContainer

## 環境構築手順

### ソースをクローンする

### .env をコピーする

```bash
cp .devcontainer/.env.sample .devcontainer/.env
```

#### VsCode でプロジェクトフォルダーを開く

### Reopen in Container を押下

Ctrl Shift P → Reopen in container と入力して実行


### 開発ツールと認証

コンテナ内で `task codex` または `task claude` を実行します。Task、Codex CLI、Claude Code、GitHub CLI を利用できます。
WSL ホストの `~/.codex` と `~/.claude` を書き込み可能で共有するため、認証だけでなく設定・履歴も共有され、コンテナからホスト側のファイルを変更できます。認証がなければ各 CLI で初回ログインしてください。GitHub の設定は読み取り専用で共有します。読み取り専用マウントは API 操作の権限を制限しません。

ホストに `~/.codex`、`~/.claude`、`~/.config/gh`、`~/.gitconfig` が必要です。

設定や Dockerfile を変更した場合は VS Code の **Dev Containers: Rebuild Container** で再構築します。既存のデータやボリュームは自動削除されません。

### ゲームのセーブを編集する

`.devcontainer/.env` の `FILE_PATH` に、編集したいセーブのフォルダーそのもの（`__builtins__.py` と `.py` ファイルがあるフォルダー）を WSL のパスで指定します。Windows 版の例は `/mnt/c/Users/<Windowsユーザー名>/AppData/LocalLow/TheFarmerWasReplaced/TheFarmerWasReplaced/Saves/Save0` です。Linux の Steam/Proton 版では `~/.steam/steam/steamapps/compatdata/2060160/pfx/drive_c/users/steamuser/AppData/LocalLow/TheFarmerWasReplaced/TheFarmerWasReplaced` の中から該当セーブを探し、絶対パスを指定してください。

セーブは書き込み可能でコンテナの `/home/dev/data/src` に直接マウントされます。リポジトリ内の `src` はマウント中は隠れ、編集はゲームのセーブに直接反映されます。VS Code の Python 拡張を使用し、個々のファイルだけでなく `src` フォルダー全体を開いてください。ゲーム内言語は Python に似ていますが、実際には Python ではありません。

ゲーム内で「ファイルウォッチャー」を有効にすると、外部で保存した既存ファイルの変更をセーブの再読み込みなしで確認できます。外部でファイルを新規作成・削除した場合はセーブの再読み込みが必要です。セーブ先を変更した場合はコンテナを再構築してください。

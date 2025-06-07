# Python仮想環境（venv）の基礎

## venvとは？
venvは、Pythonの標準ライブラリの一部として提供される仮想環境管理ツールです。プロジェクトごとに独立したPython環境を作成し、パッケージの依存関係を分離することができます。

## venvとcondaの比較

| 特徴 | venv | conda |
|------|------|-------|
| **目的** | Pythonパッケージの分離 | 言語に依存しない環境管理 |
| **インストール** | Python標準ライブラリ | 別途インストール必要 |
| **パッケージ管理** | pipのみ | pip + conda |
| **非Pythonパッケージ** | 管理不可 | 管理可能 |
| **ディスク容量** | 軽量 | 比較的大きい |
| **クロスプラットフォーム** | 制限あり | 優れている |
| **学習曲線** | 緩やか | やや急 |

## venvの基本的な使い方

```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 仮想環境の無効化
deactivate

# パッケージのインストール
pip install package_name

# パッケージの一覧を保存
pip freeze > requirements.txt

# パッケージの一括インストール
pip install -r requirements.txt
```

## venvの内部構造
```
venv/
├── Scripts/              # Windows用実行ファイル
│   ├── activate         # 仮想環境有効化スクリプト
│   ├── python.exe      # 仮想環境用Python
│   └── pip.exe         # 仮想環境用pip
├── Lib/
│   └── site-packages/   # インストールされたパッケージ
└── pyvenv.cfg          # 仮想環境の設定ファイル
```

## ベストプラクティス
1. プロジェクトのルートディレクトリに`venv`を作成
2. `.gitignore`に`venv/`を追加
3. `requirements.txt`で依存関係を管理
4. 定期的に`pip list --outdated`で更新確認
5. 仮想環境の有効化状態を確認（プロンプトに`(venv)`が表示）

## venvとcondaの使い分け

### venvを選ぶ場合
- 純粋なPythonプロジェクト
- 軽量な環境が必要
- 標準的なPythonパッケージのみ使用

### condaを選ぶ場合
- データサイエンスプロジェクト
- 非Pythonパッケージも必要
- 複雑な依存関係の管理が必要
- クロスプラットフォーム対応が重要

## 注意点
- 仮想環境を終了する場合は必ず`deactivate`コマンドを使用
- 新しいターミナルを開く場合は、再度`activate`を実行
- システムのPython環境を汚さないように注意
- パッケージのバージョンは`requirements.txt`で管理 
# AI-Powered Data Chat

## プロジェクト概要

自然言語で Snowflake のデータに問いかけられる AI チャットアプリ。  
Text-to-SQL 構成で、ユーザーの質問を SQL に変換して Snowflake に対してクエリを実行し、結果を自然言語で返す。

## 技術スタック

| レイヤー | 技術 |
| --- | --- |
| フロントエンド | Next.js (TypeScript, Tailwind CSS, App Router) |
| バックエンド | FastAPI (Python 3.11) |
| LLM | OpenAI API (gpt-4o) |
| データ | Snowflake (SNOWFLAKE_SAMPLE_DATA.TPCH_SF1) |
| インフラ(Azure) | Azure Container Apps, Azure Static Web Apps, Azure Container Registry |
| インフラ(AWS) | ECS Fargate, Amplify（Phase 3 で追加予定） |
| IaC | Terraform |
| コンテナ | Docker / Docker Compose |

## ディレクトリ構成

```txt
ai-data-chat/
├── frontend/               # Next.js
│   ├── app/
│   ├── components/
│   └── ...
├── backend/                # FastAPI
│   ├── main.py
│   ├── routers/
│   ├── services/
│   ├── .env                # git管理しない
│   └── requirements.txt
├── infra/
│   ├── azure/              # Azure用Terraform（Phase 2で追加）
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── aws/                # AWS用Terraform（Phase 3で追加）
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── docker-compose.yml
├── CLAUDE.md
└── README.md
```

## 環境変数（backend/.env）

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o
SNOWFLAKE_ACCOUNT=
SNOWFLAKE_USER=
SNOWFLAKE_PASSWORD=
SNOWFLAKE_DATABASE=SNOWFLAKE_SAMPLE_DATA
SNOWFLAKE_SCHEMA=TPCH_SF1
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
```

## 開発環境

- OS: WSL (Ubuntu)
- Node.js: v20 以上
- Python: 3.11（backend の venv 内）
- Docker Desktop (Windows) + WSL 連携

## 開発サーバー起動

```bash
# backend
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000

# frontend
cd frontend
npm run dev
```

## フェーズ別ロードマップ

### Phase 1：クイックラーン

#### ゴール：全部繋がって動く状態を作る

- [x] backend/.env の作成
- [x] FastAPI にOpenAIチャットエンドポイントを実装
- [x] FastAPI にSnowflake接続・Text-to-SQLロジックを実装
- [ ] Next.js にチャットUIを作成
- [ ] Next.js と FastAPI のAPI連携・ストリーミング表示
- [ ] Azure CLI で手動デプロイ（Container Apps + Static Web Apps）

### Phase 2：ポートフォリオ化

#### ゴール：人に見せられる・説明できる状態にする

- [ ] PDF アップロード → RAG 構成に昇華
- [ ] Azure AI Search によるベクトル検索
- [ ] 認証（NextAuth.js）
- [ ] チャット履歴（Cosmos DB 等）
- [ ] Azure 構成を Terraform 化（infra/azure/）
- [ ] GitHub Actions による CI/CD
- [ ] pytest / Jest によるテスト追加
- [ ] README 整備（構成図・技術選定理由）

### Phase 3：マルチクラウド対応

#### ゴール：AWSでも同等構成を動かせる状態にする

- [ ] AWS 用 Terraform を追加（infra/aws/）
- [ ] ECS Fargate に FastAPI をデプロイ
- [ ] Amplify に Next.js をデプロイ

## インフラ方針

- IaC ツール: Terraform
- Phase 1 は Azure CLI で手動構築・動作確認を優先
- Phase 2 で Azure 構成を Terraform 化（infra/azure/）
- Phase 3 で AWS 用 Terraform を追加（infra/aws/）
- AWS の既存知識を活かして Azure リソースを Terraform で定義する

### Azure / AWS 対応表

| Azure | AWS | 役割 |
| --- | --- | --- |
| Azure Container Apps | ECS Fargate | FastAPI ホスティング |
| Azure Static Web Apps | Amplify / CloudFront+S3 | Next.js ホスティング |
| Azure Container Registry | ECR | Docker イメージ管理 |
| Azure AI Search | OpenSearch | ベクトル検索（Phase 2以降） |

## コーディング規約

- コミットメッセージ: Conventional Commits（feat / fix / chore / docs 等）
- 環境変数は必ず .env で管理・ハードコード禁止
- 型定義を積極的に使う（TypeScript / Python 型ヒント）
- .env は絶対に git に含めない

## 参考リンク

- [Next.js 公式](https://nextjs.org/docs)
- [FastAPI 公式](https://fastapi.tiangolo.com)
- [OpenAI API 公式](https://platform.openai.com/docs)
- [Snowflake Python Connector](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector)
- [Azure Container Apps](https://learn.microsoft.com/ja-jp/azure/container-apps/)
- [Azure Static Web Apps](https://learn.microsoft.com/ja-jp/azure/static-web-apps/)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

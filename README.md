# Commander

A framework for creating commands

## Usage

```shell
pip install git+<this/repo/url>.git@<version_tag>
commander-admin startproject <project_name>
```

## Developers

```shell
git clone <this/repo/url>
cd <cloned_dir>

npm install -g opencommit
oco config set OCO_API_URL="<llm/provider/api/url>"
oco config set OCO_API_KEY="<llm_provider_api_key>"
oco config set OCO_MODEL="<desired_llm_name>"

curl -LsSf https://astral.sh/uv/0.6.14/install.sh | sh

make dependencies.install
make git.init_hooks
make help
```

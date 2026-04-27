# Travel Assistant Demo

本目录实现《Hello-Agents》第一章 1.3 的智能旅行助手示例，并补充第 4 题所要求的扩展设计。

## 安装

```bash
pip install -r requirements.txt
```

## 运行

支持直接读取当前目录下的 `.env` 文件，例如：

```env
OPENAI_API_KEY=your_key
OPENAI_BASE_URL=https://your-base-url/v1
OPENAI_MODEL=your-model
TAVILY_API_KEY=your_tavily_key
```

如果你的网关给的是带接口后缀的地址，比如 `/v1/responses`、`/chat/completions`，这个 demo 现在会自动规范化成 SDK 需要的 base URL，无需你手动改代码。

然后执行：

```bash
python main.py --city Beijing
```

如果启动后立即提示网关拦截，那么说明 `.env` 已经读到了，但你当前的 `OPENAI_BASE_URL` / `OPENAI_API_KEY` / `OPENAI_MODEL` 组合不被服务端放行，需要更换可用网关或模型名。

如需带偏好记忆：

```bash
python main.py --city Beijing --preference "historical and cultural attractions" --budget "under 200 RMB"
```

## 扩展能力

- 记忆用户偏好
- 景点售罄时自动推荐候补方案
- 连续 3 次拒绝后调整推荐策略

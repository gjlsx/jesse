# 🔑 如何获取交易所 API 密钥

## ⚠️ 重要说明
- 这些 API 密钥仅用于**获取历史数据**，不用于实盘交易
- 创建 API 密钥时，**不要**开启交易权限，只需要**读取权限**即可
- 建议使用**只读权限**的 API 密钥，更加安全

## 📋 获取步骤

### 1. Binance（币安）API 密钥

1. 访问 [Binance API 管理页面](https://www.binance.com/en/my/settings/api-management)
2. 登录你的币安账户
3. 点击 "Create API" 创建新的 API 密钥
4. 输入 API 标签名称，例如 "Jesse-Historical-Data"
5. **重要**：只勾选 "Enable Reading" （启用读取），不要勾选交易相关权限
6. 完成安全验证（邮箱、手机验证码等）
7. 复制 API Key 和 Secret Key

### 2. Bybit API 密钥

1. 访问 [Bybit API 管理页面](https://www.bybit.com/app/user/api-management)
2. 登录你的 Bybit 账户
3. 点击 "Create New Key" 创建新密钥
4. 输入密钥名称，例如 "Jesse-Data"
5. **重要**：只选择 "Read Only" 权限
6. 完成安全验证
7. 复制 API Key 和 Secret

### 3. Gate.io API 密钥

1. 访问 [Gate.io API 管理页面](https://www.gate.io/myaccount/apiv4keys)
2. 登录你的 Gate.io 账户
3. 点击 "Create API Key"
4. 输入备注，例如 "Jesse-Historical"
5. **重要**：只勾选 "Read Only" 权限
6. 完成安全验证
7. 复制 API Key 和 Secret Key

## 🛠️ 配置步骤

1. **编辑 .env 文件**：
   - 打开项目根目录下的 `.env` 文件
   - 找到对应的配置项
   - 将 "你的_API_KEY" 替换为实际的 API Key
   - 将 "你的_API_SECRET" 替换为实际的 Secret Key

2. **示例配置**：
   ```
   # Binance 期货配置
   BINANCE_PERPETUAL_FUTURES_API_KEY=abcd1234567890
   BINANCE_PERPETUAL_FUTURES_API_SECRET=xyz9876543210
   
   # Bybit 现货配置
   BYBIT_SPOT_API_KEY=efgh1111222233
   BYBIT_SPOT_API_SECRET=ijkl4444555566
   ```

3. **重启应用**：
   - 保存 `.env` 文件后
   - 停止 Jesse AI 应用（在终端按 Ctrl+C）
   - 重新启动应用

## 🚀 测试下载

配置完成后，回到浏览器：
1. 刷新页面 `http://localhost:9000`
2. 尝试重新下载历史数据
3. 如果配置正确，进度条应该开始移动

## 🔒 安全提示

1. **永远不要**在公共场所或代码仓库中暴露你的 API 密钥
2. **只使用只读权限**的 API 密钥
3. 定期更换 API 密钥
4. 如果怀疑密钥泄露，立即删除并重新创建

## ❓ 常见问题

**Q: 我没有这些交易所的账户怎么办？**
A: 你可以注册一个账户（不需要充值），仅用于获取 API 密钥下载历史数据。

**Q: 为什么需要 API 密钥？**
A: 交易所限制未认证用户的数据访问频率，API 密钥可以获得更高的访问限制。

**Q: 配置了还是下载失败怎么办？**
A: 检查密钥是否正确、网络连接是否正常，或者尝试其他交易所的数据源。

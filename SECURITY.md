# Dify Studio 安全指南

## 🔒 安全配置要求

### 1. 加密密钥配置（必需）

**生产环境必须设置加密密钥：**
```bash
# 生成安全的加密密钥（至少32位）
ENCRYPTION_SECRET_KEY=your-super-secure-encryption-key-32-chars-min
```

### 2. CORS 安全配置

**生产环境配置：**
```bash
# 只允许特定的域名访问
ALLOWED_ORIGINS=https://your-domain.com,https://app.your-domain.com
```

### 3. 数据库安全

**SQLite（开发环境）：**
```bash
DATABASE_URL=sqlite:///./dify_studio.db
```

**PostgreSQL（生产环境推荐）：**
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/dify_studio
```

### 4. 文件上传安全

- 默认文件大小限制：10MB
- 支持的文件类型应在代码中验证
- 建议在生产环境添加病毒扫描

## 🚨 安全最佳实践

### 环境变量管理
1. **不要**在代码中硬编码敏感信息
2. 使用 `.env` 文件管理配置（不要提交到版本控制）
3. 生产环境使用安全的密钥管理服务

### API 安全
1. 使用 HTTPS 协议
2. 实施速率限制
3. 验证所有输入数据
4. 使用适当的错误处理（不暴露敏感信息）

### 数据库安全
1. 使用参数化查询防止 SQL 注入
2. 定期备份数据库
3. 限制数据库访问权限

## 🔧 安全检查清单

- [ ] 设置强加密密钥（ENCRYPTION_SECRET_KEY）
- [ ] 配置正确的 CORS 域名
- [ ] 使用生产环境数据库（PostgreSQL）
- [ ] 启用 HTTPS
- [ ] 设置适当的文件上传限制
- [ ] 配置防火墙和网络访问控制
- [ ] 定期更新依赖包
- [ ] 监控和日志记录

## 📝 应急响应

如果发现安全漏洞：
1. 立即重置所有 API 密钥
2. 检查数据库是否有未授权访问
3. 更新加密密钥
4. 审查访问日志
5. 通知相关用户

## 📞 支持

如有安全问题，请立即联系开发团队。
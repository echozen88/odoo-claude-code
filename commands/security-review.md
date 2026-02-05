---
description: Odoo 19 安全审查命令 - 检测 Odoo 应用中的安全漏洞，包括访问控制问题、SQL 注入、CSRF 保护、XSS 预防和凭据管理。
---

# Odoo 19 Security Review 命令

此命令调用 **security-reviewer** agent 识别和补救 Odoo 应用中的漏洞。

## 命令功能

1. **Odoo 安全架构** - 验证访问权限、记录规则、组权限
2. **漏洞检测** - 识别 OWASP Top 10 和 Odoo 特定问题
3. **机密检测** - 查找硬编码的 API 密钥、密码、令牌
4. **输入验证** - 确保所有用户输入正确清理
5. **认证/授权** - 验证正确的访问控制
6. **SQL 注入预防** - 确保 ORM 使用而非原始 SQL
7. **XSS 预防** - 验证视图中的正确输出转义

## 使用场景

当以下情况时使用 `/security-review`：
- 编写处理用户输入的 Odoo 代码
- 实现认证或 API 端点
- 处理敏感数据
- 修改访问控制
- 准备部署到生产环境

## 工作流程

### 1. 初始扫描阶段
```bash
# 检查硬编码机密
grep -rE "(api_key|password|secret|token|aws_key)" --include="*.py" .

# 检查 sudo() 使用
grep -r "\.sudo()" --include="*.py" .

# 检查直接 SQL
grep -r "\.cr\.execute" --include="*.py" .

# 检查缺少访问权限
ls security/ir.model.access.csv || echo "缺少访问权限文件"

# 检查 XML 安全问题
grep -r "t-raw" --include="*.xml" .
```

### 2. 模型安全审查
对于每个模型：
- [ ] security/ir.model.access.csv 中定义的访问权限
- [ ] 多用户数据的记录规则
- [ ] 没有 sudo() 除非有理由
- [ ] 计算字段使用 @api.depends
- [ ] 定义了关键字段的约束

### 3. 控制器安全审查
对于每个控制器：
- [ ] 正确的 auth 参数（public/user/user_api_key）
- [ ] HTTP 路由的 CSRF 保护
- [ ] 输入验证
- [ ] 错误处理（没有给用户的堆栈跟踪）
- [ ] 公共端点的速率限制

### 4. 视图安全审查
对于每个视图：
- [ ] 没有用户输入的 t-raw
- [ ] 正确的字段访问控制
- [ ] 隐藏字段中没有敏感数据
- [ ] 动态内容的正确转义

## 关键漏洞检测

### 1. SQL 注入（CRITICAL）

```python
# ❌ CRITICAL: SQL 注入漏洞
query = f"SELECT * FROM table WHERE id = {user_input}"
self.env.cr.execute(query)

# ❌ CRITICAL: 通过格式字符串的 SQL 注入
query = "SELECT * FROM table WHERE name = '{}'".format(user_input)
self.env.cr.execute(query)

# ✅ CORRECT: 使用 ORM
records = self.env['table'].search([('id', '=', user_input)])

# ✅ CORRECT: 使用参数化查询（当 SQL 必要时）
self.env.cr.execute("SELECT * FROM table WHERE id = %s", (user_input,))
```

### 2. 访问控制绕过（CRITICAL）

```python
# ❌ CRITICAL: sudo() 绕过所有安全检查
def action_approve(self):
    self.sudo().write({'state': 'approved'})
    # 任何人都可以批准任何东西！

# ✅ CORRECT: 只在必要时使用 sudo
def action_technical_cleanup(self):
    # 应该绕过访问权限的技术清理
    self.sudo()._cleanup_old_records()
    # 记录为什么使用 sudo
```

### 3. 缺少访问权限（CRITICAL）

```python
# ❌ CRITICAL: 没有访问权限的模型
class MySecretData(models.Model):
    _name = 'my.secret.data'
    # 没有 ir.model.access.csv 条目意味着没人可以访问

# ✅ CORRECT: 在 security/ir.model.access.csv 中定义访问权限
access_my_secret_data_user,my.secret.data,my_module.group_user,1,1,0,0
```

### 4. 缺少记录规则（CRITICAL）

```python
# ❌ CRITICAL: 没有记录规则的多用户模型
class UserNote(models.Model):
    _name = 'user.note'
    user_id = fields.Many2one('res.users', required=True)
    # 任何人都可以读取任何人的笔记！

# ✅ CORRECT: 在 security/security.xml 中添加记录规则
<record id="rule_user_note_own" model="ir.rule">
    <field name="domain_force">[('user_id', '=', user.id)]</field>
    <field name="model_id" ref="model_user_note"/>
</record>
```

### 5. 缺少 CSRF 保护（CRITICAL）

```python
# ❌ CRITICAL: 没有 CSRF 保护的 POST 路由
@http.route('/my/action', type='http', methods=['POST'], auth='user')
def my_action(self, **kwargs):
    # 易受 CSRF 攻击！

# ✅ CORRECT: 对公共表单使用 auth='public' 和 CSRF 令牌
@http.route('/my/action', type='http', methods=['POST'], auth='public', csrf=True)
def my_action(self, **kwargs):
    token = kwargs.get('csrf_token')
    # 验证令牌

# ✅ CORRECT: JSON 类型自动处理 CSRF
@http.route('/my/action', type='json', auth='user')
def my_action(self, **kwargs):
    # 内置 CSRF 保护
```

### 6. 硬编码机密（CRITICAL）

```python
# ❌ CRITICAL: 硬编码机密
API_KEY = "sk-proj-xxxxx"
DB_PASSWORD = "admin123"
TOKEN = "ghp_xxxxxxxxxxxx"

# ✅ CORRECT: 使用环境变量或系统参数
import os

API_KEY = os.environ.get('MY_API_KEY')
if not API_KEY:
    raise UserError(_("API key not configured"))

# 或使用 Odoo 系统参数
API_KEY = self.env['ir.config_parameter'].sudo().get_param('my_module.api_key')
```

### 7. QWeb 模板中的 XSS（HIGH）

```xml
<!-- ❌ HIGH: XSS 漏洞 -->
<t t-esc="user_input"/>

<!-- ❌ HIGH: 属性中的 XSS -->
<a t-att-href="user_input">Link</a>

<!-- ✅ CORRECT: 使用 t-esc（默认转义）或谨慎使用 t-raw -->
<t t-esc="user_input"/>

<!-- ✅ CORRECT: 清理或验证 URL -->
<a t-att-href="validate_url(user_input)">Link</a>
```

### 8. 缺少输入验证（HIGH）

```python
# ❌ HIGH: 没有验证
@http.route('/api/data', type='json', auth='user')
def api_data(self, data):
    return self.env['model'].search([('name', '=', data['query'])])

# ✅ CORRECT: 验证输入
@http.route('/api/data', type='json', auth='user')
def api_data(self, data):
    query = data.get('query')
    if not query or len(query) > 100:
        raise UserError(_("Invalid query"))
    return self.env['model'].search([('name', '=', query)])
```

## Odoo 安全架构审查

### 1. 访问权限（ir.model.access）
```python
# 检查 security/ir.model.access.csv 中缺少的访问权限
access_model_user,model_name,base.group_user,1,1,1,1
#                        ^^^^^^^^^^^^^^
#                        可以访问的组

# 格式: id,model_id,group_id,perm_read,perm_write,perm_create,perm_unlink
```

**检查清单:**
- [ ] 所有模型都有访问权限定义
- [ ] 组分配适当（不要太宽松）
- [ ] 管理员访问限制为正确的组
- [ ] 没有敏感数据的全局读/写访问

### 2. 记录规则（ir.rule）
```xml
<record id="rule_my_model_user" model="ir.rule">
    <field name="name">My Model: User Records Only</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="domain_force">[('user_id', '=', user.id)]</field>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
    <field name="perm_read" eval="True"/>
    <field name="perm_write" eval="True"/>
    <field name="perm_create" eval="True"/>
    <field name="perm_unlink" eval="True"/>
</record>
```

**检查清单:**
- [ ] 多用户模型有记录规则
- [ ] 用户只能访问自己的记录（适当情况下）
- [ ] 没有过于宽松的规则如 `[(1, '=', 1)]`
- [ ] 管理员组在需要时有更广泛的访问
- [ ] 规则不冲突

### 3. 安全组
```xml
<record id="group_my_module_user" model="res.groups">
    <field name="name">My Module User</field>
    <field name="category_id" ref="module_category"/>
    <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
</record>
```

**检查清单:**
- [ ] 组遵循 Odoo 约定
- [ ] 类别正确设置
- [ ] 组层级逻辑（implied_groups）
- [ ] 访问是最小权限原则

## OWASP Top 10 Odoo 分析

### A01:2021 - 访问控制失效

**Odoo 特定检查:**
- [ ] 记录规则防止跨租户数据访问
- [ ] sudo() 只在绝对必要时使用
- [ ] 组正确限制管理功能
- [ ] API 端点验证用户权限

### A02:2021 - 加密故障

**检查:**
- [ ] 生产环境强制 HTTPS
- [ ] 没有明文密码
- [ ] 敏感数据静态加密
- [ ] 环境变量或系统参数中的机密

### A03:2021 - 注入

**Odoo 特定检查:**
- [ ] 所有查询使用 ORM（没有理由的直接 SQL）
- [ ] 域表达式使用参数化格式
- [ ] 查询中没有字符串连接

### A04:2021 - 不安全设计

**检查:**
- [ ] 从设计考虑安全
- [ ] 多租户隔离
- [ ] 最小权限原则

### A05:2021 - 安全配置错误

**Odoo 特定检查:**
- [ ] 生产环境禁用调试模式
- [ ] 数据库凭据没有硬编码
- [ ] 正确的文件权限
- [ ] 日志文件不公开访问

### A06:2021 - 易受攻击组件

**检查:**
- [ ] 依赖项最新
- [ ] Odoo 模块来自可信来源
- [ ] 定期安全审计

### A07:2021 - 认证失效

**Odoo 特定检查:**
- [ ] 正确的认证流程
- [ ] 会话管理安全
- [ ] 强制执行密码策略

### A08:2021 - 软件和数据完整性失效

**检查:**
- [ ] 数据完整性约束
- [ ] 敏感操作的审计日志
- [ ] 不可变审计跟踪

### A09:2021 - 安全日志故障

**Odoo 特定检查:**
- [ ] 记录安全事件
- [ ] 日志不暴露给用户
- [ ] 配置日志轮换

### A10:2021 - 服务器端请求伪造（SSRF）

**检查:**
- [ ] 外部请求的 URL 验证
- [ ] 允许域名的白名单
- [ ] 为外部调用配置超时

## 安全审查报告格式

```markdown
# Odoo 安全审查报告

**模块:** [odoo_module_name]
**审查日期:** YYYY-MM-DD
**审查者:** security-reviewer agent

## 摘要
- **关键问题:** X
- **高优先级问题:** Y
- **中等优先级问题:** Z
- **低优先级问题:** W
- **风险级别:** 🔴 高 / 🟡 中 / 🟢 低

## 关键问题（立即修复）

### 1. SQL 注入漏洞
**严重性:** CRITICAL
**类别:** A03: 注入
**位置:** `models/my_model.py:45`

**问题:**
用户输入在没有清理的情况下连接到 SQL 查询中。

**影响:**
攻击者可以执行任意 SQL 命令，可能访问、修改或删除所有数据。

**概念验证:**
```python
# 如果 user_input = "1; DROP TABLE my_model; --"
query = f"SELECT * FROM my_model WHERE id = {user_input}"
# 结果: SELECT * FROM my_model WHERE id = 1; DROP TABLE my_model; --
```

**补救:**
```python
# ✅ 使用 ORM 代替
records = self.env['my.model'].search([('id', '=', user_input)])

# ✅ 或使用参数化查询
self.env.cr.execute("SELECT * FROM my_model WHERE id = %s", (user_input,))
```

**参考:**
- OWASP A03:2021 - 注入
- CWE-89: SQL 注入

### 2. 缺少访问权限
**严重性:** CRITICAL
**类别:** A01: 访问控制失效
**位置:** `security/ir.model.access.csv`

**问题:**
模型 `my.secret.model` 没有定义访问权限。

**影响:**
没有用户（包括管理员）可以访问此模型，使功能不可用。或者如果使用 sudo() 绕过，这是一个安全漏洞。

**补救:**
添加到 `security/ir.model.access.csv`:
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_secret_user,my.secret.model,base.group_user,1,1,1,0
access_my_secret_manager,my.secret.model,my_module.group_manager,1,1,1,1
```

### 3. 多用户数据缺少记录规则
**严重性:** CRITICAL
**类别:** A01: 访问控制失效
**位置:** `models/user_note.py`

**问题:**
多用户模型 `user.note` 没有定义记录规则。

**影响:**
用户可以读取/修改/删除属于其他用户的笔记。

**补救:**
添加到 `security/security.xml`:
```xml
<odoo>
    <data noupdate="1">
        <record id="rule_user_note_own" model="ir.rule">
            <field name="name">User Note: Own Records Only</field>
            <field name="model_id" ref="model_user_note"/>
            <field name="domain_force">[('user_id', '=', user.id)]</field>
            <field name="groups" eval="[(4, ref('base.group_user'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="True"/>
            <field name="perm_create" eval="True"/>
            <field name="perm_unlink" eval="True"/>
        </record>
    </data>
</odoo>
```

## 高优先级问题（生产前修复）

### 1. 不必要的 sudo() 使用
**严重性:** HIGH
**类别:** A01: 访问控制失效
**位置:** `controllers/controller.py:23`

**问题:**
控制器不必要地使用 sudo() 绕过安全检查。

**补救:**
```python
# ❌ 移除 sudo()
def my_action(self):
    self.sudo().write({'state': 'approved'})

# ✅ 让安全规则应用
def my_action(self):
    self.write({'state': 'approved'})
```

## Odoo 安全检查清单

### 访问控制
- [ ] 所有模型都有访问权限（ir.model.access.csv）
- [ ] 多用户模型有记录规则（ir.rule）
- [ ] sudo() 只在绝对必要时使用
- [ ] 组权限遵循最小权限原则
- [ ] 管理操作限制为系统组

### 输入验证
- [ ] 所有用户输入已验证
- [ ] 字符串输入的长度限制
- [ ] 数值输入的类型检查
- [ ] 外部调用的 URL/域验证

### SQL 安全
- [ ] 查询中没有字符串连接
- [ ] 所有查询使用 ORM（理由除外）
- [ ] 原始 SQL 的参数化查询
- [ ] 查询中没有动态表/列名

### 输出编码
- [ ] QWeb 中用户输入没有 t-raw
- [ ] 属性中使用的 URL 已验证
- [ ] 错误消息中没有敏感数据
- [ ] 用户没有堆栈跟踪

### 认证和授权
- [ ] HTTP POST 路由的 CSRF 保护
- [ ] 所有路由上正确的 auth 参数
- [ ] 会话管理安全
- [ ] 强制执行密码策略

### 机密管理
- [ ] 没有硬编码的 API 密钥、密码、令牌
- [ ] 环境变量或系统参数中的机密
- [ ] Git 历史中没有机密
- [ ] 日志中没有机密

### 日志和监控
- [ ] 记录安全事件
- [ ] 带上下文的错误日志
- [ ] 日志不包含敏感数据
- [ ] 日志文件正确保护

## 建议

1. 启用 Odoo 的内置安全审计
2. 发布前定期安全审查
3. 在 CI/CD 中实施安全测试
4. 使用 bandit 等工具进行静态分析
5. 监控 Odoo SAAS 的安全公告
6. 保持 Odoo 和依赖项最新

## 工具

```bash
# Python 安全扫描器
pip install bandit
bandit -r odoo_module/

# 检查机密
pip install trufflehog
trufflehog filesystem .

# 依赖漏洞检查
pip install safety
safety check -r requirements.txt
```

## 应急响应

如果发现关键漏洞：

1. **记录** - 创建带有 PoC 的详细报告
2. **通知** - 立即通知项目所有者
3. **建议修复** - 提供安全代码示例
4. **测试修复** - 验证补救有效
5. **验证影响** - 检查漏洞是否被利用
6. **轮换机密** - 如果凭据暴露

## 成功指标

安全审查后：
- ✅ 未发现关键问题
- ✅ 所有高优先级问题已解决
- ✅ 安全检查清单完成
- ✅ 代码中没有机密
- ✅ 正确配置访问权限
- ✅ 为多用户模型定义记录规则
- ✅ 测试包括安全场景
```

## 与其他命令的集成

- 使用 `/plan` 首先规划实施
- 使用 `/tdd` 以测试驱动方式实施
- 使用 `/code-review` 审查实施
- 使用 `/security-review` 进行安全审查

## 相关 Agent

此命令调用位于以下位置的 `security-reviewer` agent：
`~/.claude/agents/security-reviewer.md`

## 记住

安全对于 Odoo 应用至关重要，特别是当处理敏感业务数据时。一个漏洞可能导致数据泄露、财务损失或合规违规。要彻底、要偏执、要主动。

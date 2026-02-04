**Language:** English | [简体中文](README.zh-CN.md)

# Odoo Claude Code

[![Stars](https://img.shields.io/github/stars/echozen88/odoo-claude-code?style=flat)](https://github.com/echozen88/odoo-claude-code/stargazers)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white)
![Shell](https://img.shields.io/badge/-Shell-4EAA25?logo=gnu-bash&logoColor=white)

---

<div align="center">

**🌐 Language / 语言**

[**English**](README.md) | [简体中文](README.zh-CN.md)

</div>

---

**专门为 Odoo 19 开发定制的 Claude Code 插件。**

为 Odoo ERP 框架量身定制的生产就绪的代理、技能、钩子、命令和规则。

---

## 与原版的区别

本插件将强大的 `everything-claude-code` 工作流专门适配 Odoo 19 开发：

### Odoo 特有功能
- **Odoo 19 规划**：模块结构、模型/视图/控制器规划
- **Odoo ORM 指导**：字段类型、关系、计算字段
- **Odoo 安全**：访问权限、记录规则、SQL 注入防护
- **Odoo 测试**：TransactionCase、HttpCase、安全测试
- **Odoo 视图**：树视图、表单视图、看板视图、透视表、QWeb 模板

### 编排工作流
```bash
/orchestrate feature "添加新的销售报告模块"

执行流程：
planner (Odoo 19) → tdd-guide (Odoo 测试) →
code-reviewer (Odoo 代码风格) → security-reviewer (Odoo 安全) →
odoo-reviewer (Odoo 框架)
```

---

## 快速开始

### 步骤 1：安装插件

```bash
# 添加市场
/plugin marketplace add echozen88/odoo-claude-code

# 安装插件
/plugin install odoo-claude-code@odoo-claude-code
```

### 步骤 2：安装规则（必需）

> ⚠️ **重要**：Claude Code 插件系统无法自动分发 `rules`。需要手动安装：

```bash
# 首先克隆仓库
git clone https://github.com/echozen88/odoo-claude-code.git

# 复制规则（应用于所有项目）
cp -r odoo-claude-code/rules/* ~/.claude/rules/
```

### 步骤 3：开始使用

```bash
# 尝试编排命令
/orchestrate feature "添加一个带有自定义字段的新 Odoo 模块"

# 规划一个 Odoo 功能
/plan "创建一个用于批量订单处理的向导"

# Odoo 模型的 TDD 工作流
/tdd "实现带有约束的 Odoo 模型"

# 代码审查
/code-review

# 安全审查
/security-review
```

---

## 插件结构

```
odoo-claude-code/
├── .claude-plugin/   # 插件和市场清单
│   ├── plugin.json         # 插件元数据和组件路径
│   └── marketplace.json    # 市场目录
│
├── agents/           # Odoo 19 专用子代理
│   ├── planner.md           # Odoo 功能实施规划
│   ├── tdd-guide.md         # Odoo 测试驱动开发
│   ├── code-reviewer.md     # Odoo 代码质量审查
│   ├── security-reviewer.md  # Odoo 安全审查
│   └── odoo-reviewer.md     # Odoo 框架合规审查
│
├── skills/           # Odoo 领域知识
│   ├── odoo-patterns/       # Odoo 模块结构与约定
│   ├── odoo-orm/           # ORM 使用与最佳实践
│   ├── odoo-views/         # 视图、QWeb、模板
│   └── odoo-security/      # Odoo 安全模式
│
├── commands/         # Odoo 专用命令
│   └── orchestrate.md       # 编排工作流
│
├── rules/            # Odoo 编码规范
│   ├── odoo-coding-style.md    # PEP8、命名、组织
│   ├── odoo-security.md        # 访问权限、记录规则
│   ├── odoo-testing.md         # 测试需求与模式
│   └── odoo-api.md            # API 开发规则
│
└── hooks/            # Odoo 专用自动化
    └── hooks.json                # PreToolUse、PostToolUse、Stop 钩子
```

---

## 编排工作流

`/orchestrate` 命令为 Odoo 19 开发提供完整的开发工作流：

### 功能开发工作流
```
planner → tdd-guide → code-reviewer → security-reviewer → odoo-reviewer
```
- 规划 Odoo 模块结构
- 先写测试（TDD）
- 审查 Odoo 编码规范
- 安全审计（访问权限、记录规则）
- 框架合规检查

### Bug 修复工作流
```
explorer → tdd-guide → code-reviewer → odoo-reviewer
```
- 调查 Odoo Bug
- 修复并测试
- 审查更改

### 安全审查工作流
```
security-reviewer → code-reviewer → odoo-reviewer → architect
```
- 专注安全审查
- Odoo 的 OWASP Top 10
- 访问控制验证

---

## Odoo 19 功能覆盖

### 模块结构
- `__manifest__.py` 配置
- 模型、视图、控制器组织
- 安全组和记录规则

### 模型开发
- 字段类型（Char、Text、Many2one、One2many 等）
- 带有 `@api.depends` 的计算字段
- Onchange 方法
- 约束
- 继承模式

### 视图
- 带有装饰和按钮的树视图
- 带有笔记本和工作表的表单视图
- 看板视图
- 透视表和图表视图
- QWeb 模板

### 安全
- 访问权限（ir.model.access.csv）
- 记录规则（ir.rule）
- CSRF 保护
- QWeb 中的 XSS 防护

### 测试
- 模型测试的 TransactionCase
- 控制器测试的 HttpCase
- 安全测试模式

---

## 系统要求

### Claude Code CLI 版本

**最低版本：v2.1.0 或更高**

检查您的版本：
```bash
claude --version
```

---

## 安装

### 方式 1：作为插件安装（推荐）

```bash
# 添加此仓库为市场
/plugin marketplace add echozen88/odoo-claude-code

# 安装插件
/plugin install odoo-claude-code@odoo-claude-code
```

或直接添加到您的 `~/.claude/settings.json`：

```json
{
  "extraKnownMarketplaces": {
    "odoo-claude-code": {
      "source": {
        "source": "github",
        "repo": "echozen88/odoo-claude-code"
      }
    }
  },
  "enabledPlugins": {
    "odoo-claude-code@odoo-claude-code": true
  }
}
```

这将使您可以立即访问所有命令、代理、技能和钩子。

> **注意**：Claude Code 插件系统不支持通过插件分发 `rules`（[上游限制](https://code.claude.com/docs/en/plugins-reference)）。您需要手动安装规则：
>
> ```bash
> # 首先克隆仓库
> git clone https://github.com/echozen88/odoo-claude-code.git
>
> # 方式 A：用户级规则（应用于所有项目）
> cp -r odoo-claude-code/rules/* ~/.claude/rules/
>
>
> # 方式 B：项目级规则（仅应用于当前项目）
> mkdir -p .claude/rules
> cp -r odoo-claude-code/rules/* .claude/rules/
> ```

---

### 方式 2：手动安装

```bash
# 克隆仓库
git clone https://github.com/echozen88/odoo-claude-code.git

# 复制代理
cp odoo-claude-code/agents/*.md ~/.claude/agents/

# 复制规则（必需）
cp odoo-claude-code/rules/*.md ~/.claude/rules/

# 复制命令
cp odoo-claude-code/commands/*.md ~/.claude/commands/

# 复制技能
cp -r odoo-claude-code/skills/* ~/.claude/skills/

# 复制钩子（可选，在 plugin.json 中）
# hooks 自动从 hooks/hooks.json 加载
```

#### 在 settings.json 中添加钩子
将 `hooks/hooks.json` 中的钩子复制到您的 `~/.claude/settings.json`。

#### 配置 MCP
将 `mcp-configs/mcp-servers.json` 中所需的 MCP 服务器复制到您的 `~/.claude.json`。

**重要：** 使用您的实际 API 密钥替换 `YOUR_*_HERE` 占位符。
```

---

## 代理说明

### planner (Odoo 19)
Odoo 模块专家规划代理。创建包含以下内容的实施计划：
- 模型定义和继承
- 视图需求
- 安全设置（组、访问权限、记录规则）
- 数据迁移考虑

### tdd-guide (Odoo 19)
Odoo 的测试驱动开发专家：
- 模型测试的 TransactionCase 模式
- 控制器测试的 HttpCase 模式
- 安全测试模式
- 80%+ 覆盖率要求

### code-reviewer (Odoo 19)
带有 Odoo 特定检查的代码质量审查员：
- PEP8 合规性
- API 装饰器使用
- 字段定义
- 视图结构

### security-reviewer (Odoo 19)
Odoo 应用的安全专家：
- 访问权限验证
- 记录规则分析
- SQL 注入防护
- QWeb 中的 XSS 防护
- CSRF 保护

### odoo-reviewer (Odoo 19)
框架合规专家：
- Manifest 配置
- 模块结构
- 继承模式
- Odoo 约定

---

## 可用技能

### odoo-patterns
模块结构、命名约定、视图模式

### odoo-orm
字段类型、关系、搜索/写入操作、计算字段

### odoo-views
树视图、表单视图、看板视图、透视表、QWeb 模板

### odoo-security
访问权限、记录规则、控制器安全

---

## 可用命令

| 命令 | 描述 |
|---------|-------------|
| `/orchestrate feature` | Odoo 功能开发完整工作流 |
| `/orchestrate bugfix` | Odoo Bug 调查工作流 |
| `/orchestrate security` | Odoo 安全审查工作流 |
| `/plan` | 创建 Odoo 实施计划 |
| `/tdd` | Odoo 测试驱动开发 |
| `/code-review` | Odoo 代码质量审查 |
| `/security-review` | Odoo 安全审查 |

---

## 使用示例

### 规划 Odoo 模块

```bash
/plan "创建一个带有自定义字段的销售订单明细"
```

输出包括：
- 带有字段定义的模型结构
- 所需视图（树视图、表单视图、看板视图）
- 安全组和访问权限
- 多用户数据的记录规则
- 迁移考虑

### 使用 TDD 实现

```bash
/tdd "实现带有验证的销售订单模型"
```

工作流：
1. 先编写失败的测试
2. 实现代码以通过测试
3. 重构代码
4. 验证 80%+ 覆盖率

### 编排功能

```bash
/orchestrate feature "为采购订单添加审批工作流"
```

完整工作流执行：
1. **Planner**：创建实施计划
2. **TDD Guide**：编写测试、实现代码
3. **Code Reviewer**：审查质量
4. **Security Reviewer**：审计安全性
5. **Odoo Reviewer**：框架合规
6. **最终报告**：总结和建议

---

## Odoo 19 快速参考

### 模块命名
- 格式：`my_module_name`
- 模型格式：`module.model_name`

### 字段命名
- Many2one：`name_id`
- One2many：`line_ids`
- Many2many：`tag_ids`

### 常用依赖
- `base` - Odoo 核心模型
- `web` - 前端框架
- `mail` - 消息传递
- `sale` - 销售订单
- `purchase` - 采购订单

### API 装饰器
```python
@api.model           # 模型方法
@api.depends(*fields)  # 计算字段
@api.onchange(*fields)  # Onchange 处理器
@api.constrains(*fields)  # 约束验证
```

---

## 贡献

**欢迎贡献！**

如果您有：
- Odoo 特定模式
- 更好的安全规则
- 额外的测试策略
- 框架特定的改进

请贡献！

---

## 相关链接

- **基于**：[Everything Claude Code](https://github.com/affaan-m/everything-claude-code)
- **Odoo 19 文档**：https://www.odoo.com/documentation/17.0/
- **Odoo 开发者论坛**：https://www.odoo.com/forum

---

## 许可证

MIT - 可自由使用、修改需要时修改，可以贡献。

---

**如果对您有帮助，请点亮 Star。祝 Odoo 开发愉快！**

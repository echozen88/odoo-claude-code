# Odoo Patterns Skill 文件结构说明

本文档描述 `SKILL.md` 文件中各个部分的作用和用途。

---

## 文件概述

**文件路径**: `skills/odoo-patterns/SKILL.md`
**总行数**: 约 682 行
**用途**: 为 Odoo 19 模块开发提供全面的模式和约定指南

---

## 各部分详解

### 1. 标题与简介 (Lines 1-3)

```
# Odoo 19 Development Patterns
```

**作用**: 声明此 skill 的主题和适用范围（Odoo 19 版本）

---

### 2. Module Structure 模块结构 (Lines 5-59)

**作用**: 定义标准 Odoo 19 模块的目录结构

**包含内容**:
- 完整的模块目录树
- 每个目录/文件的用途注释
- 标准 11 个核心目录：
  - `__manifest__.py` - 模块清单
  - `models/` - 模型定义
  - `views/` - 视图 XML
  - `security/` - 访问控制
  - `controllers/` - HTTP 控制器
  - `static/` - 静态资源
  - `data/` - 数据记录
  - `demo/` - 演示数据
  - `wizard/` - 向导（临时模型）
  - `report/` - 报表
  - `tests/` - 测试
  - `i18n/` - 翻译
  - `lib/` - 工具库

---

### 3. Naming Conventions 命名约定 (Lines 61-86)

**作用**: 规范 Odoo 开发中的命名标准

**涵盖类型**:
| 类别 | 格式 | 示例 |
|------|------|------|
| 模块名 | `lowercase_with_underscores` | `my_custom_module` |
| 模型名 | `module.model_name` | `sale.order` |
| Many2one 字段 | `name_id` | `partner_id` |
| One2many 字段 | `name_ids` | `order_line_ids` |
| Many2many 字段 | `name_ids` | `tag_ids` |
| XML ID | `module.resource_type.name` | `module.view_model_form` |

---

### 4. Module Manifest Pattern 模块清单模式 (Lines 87-185)

**作用**: 定义 `__manifest__.py` 的完整结构和最佳实践

**包含两个示例**:
1. **通用模板** (Lines 87-143) - 带注释的完整清单结构
2. **实际示例** (Lines 145-185) - Partner Approval State 模块的真实案例

**关键字段说明**:
- `version`: 版本号格式 `19.0.1.0.0`
- `depends`: 依赖模块列表
- `data`: 数据文件加载顺序
- `assets`: 静态资源打包
- `qweb`: QWeb 模板
- `demo`: 演示数据
- `installable`: 是否可安装
- `application`: 是否为应用（显示在应用列表）
- `auto_install`: 是否自动安装
- `post_init_hook`: 安装后钩子
- `uninstall_hook`: 卸载钩子

---

### 5. Model Definition Patterns 模型定义模式 (Lines 187-303)

**作用**: 提供各种模型类型的定义模板

**包含 4 种模型类型**:

#### 5.1 Basic Model 基础模型 (Lines 189-246)
- 常用字段类型
- 关系字段
- 计算字段
- SQL 约束
- Python 约束

#### 5.2 Model Inheritance 模型继承 (Lines 248-269)
- 类扩展 (_inherit)
- 原型继承 (_inherit + _name)

#### 5.3 Abstract Model 抽象模型 (Lines 271-283)
- 用于复用字段和方法的基类

#### 5.4 Transient Model 临时模型/向导 (Lines 285-303)
- TransientModel 专用
- 自动清理机制

---

### 6. View Definition Patterns 视图定义模式 (Lines 305-453)

**作用**: 定义各种视图类型的 XML 结构

**包含 6 种视图类型**:

| 视图类型 | 用途 | 关键属性 |
|----------|------|----------|
| Tree View | 列表视图 | multi_edit, limit, decoration-* |
| Form View | 表单视图 | header, sheet, notebook, chatter |
| Kanban View | 看板视图 | default_group_by, quick_create |
| Pivot View | 透视表 | interval, type=row/col/measure |
| Graph View | 图表视图 | type=row/measure |
| Search View | 搜索视图 | filters, groups |

---

### 7. View Inheritance Patterns 视图继承模式 (Lines 455-488)

**作用**: 展示如何扩展现有视图

**关键技术**:
- `<field>` 标签的 `position` 属性
- `<xpath>` 高级定位表达式

**Position 值**:
- `after` - 在目标后插入
- `before` - 在目标前插入
- `inside` - 在目标内插入
- `replace` - 替换目标
- `attributes` - 修改目标属性

---

### 8. Controller Patterns 控制器模式 (Lines 489-522)

**作用**: 定义 HTTP 控制器和路由

**包含 3 种路由类型**:
1. **HTTP 路由** - 网页渲染
2. **JSON 路由** - API 调用
3. **POST 路由** - 表单提交（带 CSRF 保护）

**关键装饰器参数**:
- `type`: 'http' / 'json'
- `auth`: 'public' / 'user' / 'user_api_key'
- `methods`: HTTP 方法
- `csrf`: CSRF 保护
- `website`: 网站集成

---

### 9. Action Patterns 动作模式 (Lines 524-560)

**作用**: 定义 Odoo 动作类型

**包含 3 种动作类型**:
1. **Window Action** (ir.actions.act_window) - 打开视图
2. **Server Action** (ir.actions.server) - 执行服务器代码
3. **Client Action** (ir.actions.client) - 触发客户端操作

---

### 10. Menu Patterns 菜单模式 (Lines 562-580)

**作用**: 定义菜单结构

**菜单层次**:
- 根菜单 (Root Menu)
- 子菜单 (Child Menu)
- 动作关联 (action 属性)

---

### 11. Common Patterns 通用模式 (Lines 582-668)

**作用**: 提供 Odoo 开发中常见场景的实现模式

**包含 7 种常见模式**:

| 模式 | 说明 |
|------|------|
| Workflow State Machine | 状态机工作流 |
| Chatter Integration | 消息/活动集成 |
| Multi-Company Support | 多公司支持 |
| Sequences | 自动序列号 |
| Attachments | 附件管理 |

---

### 12. Best Practices 最佳实践 (Lines 670-682)

**作用**: 总结 10 条核心开发原则

**最佳实践列表**:
1. 始终使用 ORM
2. 使用装饰器 (@api.*)
3. 翻译用户字符串 (_())
4. 遵循命名约定
5. 安全优先
6. 充分测试
7. 文档化代码
8. 错误处理
9. 正确使用继承
10. 考虑多公司

---

## 文件结构总结

```
SKILL.md
├── 1. 标题与简介
├── 2. Module Structure (目录结构)
├── 3. Naming Conventions (命名约定)
├── 4. Module Manifest Pattern (清单文件)
├── 5. Model Definition Patterns (模型定义)
│   ├── Basic Model
│   ├── Model Inheritance
│   ├── Abstract Model
│   └── Transient Model
├── 6. View Definition Patterns (视图定义)
│   ├── Tree View
│   ├── Form View
│   ├── Kanban View
│   ├── Pivot View
│   ├── Graph View
│   └── Search View
├── 7. View Inheritance Patterns (视图继承)
├── 8. Controller Patterns (控制器)
├── 9. Action Patterns (动作)
├── 10. Menu Patterns (菜单)
├── 11. Common Patterns (通用模式)
└── 12. Best Practices (最佳实践)
```

---

## 使用场景

此 skill 文件在以下情况下被调用：

1. **创建新模块** - 使用 Module Structure 和 Manifest Pattern
2. **定义模型** - 使用 Model Definition Patterns
3. **创建视图** - 使用 View Definition Patterns
4. **扩展现有功能** - 使用 View Inheritance Patterns
5. **添加 API 端点** - 使用 Controller Patterns
6. **实现工作流** - 使用 Common Patterns 中的 State Machine

---

## 相关文件

- **Agent**: `agents/planner.md` - 功能规划时使用此 skill
- **Agent**: `agents/code-reviewer.md` - 代码审查时参考此 skill 的最佳实践
- **Rule**: `rules/odoo-coding-style.md` - 编码规范规则
- **Command**: `commands/scaffold.md` - 脚手架命令使用此 skill 生成模板

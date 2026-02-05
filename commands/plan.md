---
description: Odoo 19 功能规划命令 - 重新评估需求、识别风险、创建分步实施计划。在修改任何代码前等待用户确认。
---

# Odoo 19 Plan 命令

此命令调用 **planner** agent 为 Odoo 19 模块和功能创建全面的实施计划。

## 命令功能

1. **重新评估需求** - 明确需要构建的 Odoo 功能
2. **识别风险** - 提出潜在问题和阻塞因素
3. **创建分步计划** - 将实施分解为多个阶段
4. **等待确认** - 必须收到用户明确批准才能继续

## 使用场景

当以下情况时使用 `/plan`：
- 开始新的 Odoo 模块开发
- 进行重大的 Odoo 架构变更
- 处理复杂的 Odoo 代码重构
- 多个文件/组件将受到影响
- 需求不明确或存在歧义

## 工作原理

planner agent 将执行以下操作：

1. **分析请求** 并用清晰的术语重述 Odoo 需求
2. **分解为阶段** 包含具体的可操作步骤
3. **识别组件间依赖**（模型、视图、控制器、安全）
4. **评估风险** 和潜在的阻塞因素
5. **估算复杂度**（高/中/低）
6. **展示计划** 并等待您的明确确认

## Odoo 19 规划关键要素

### 模块结构规划
- `__manifest__.py` - 模块清单和依赖
- `models/` - 模型定义（继承 vs 新建）
- `views/` - XML 视图定义（tree、form、kanban、pivot、graph）
- `security/` - 访问控制（ir.model.access.csv、ir.rule）
- `controllers/` - HTTP 路由和控制器
- `static/` - OWL 组件、CSS、QWeb 模板

### 模型设计规划
- 新模型命名：`module.model_name`
- 继承模型：`_inherit = 'existing.model'`
- 字段类型：Char、Text、Many2one、One2many、Many2many
- 计算字段：`@api.depends` 装饰器
- 约束：`@api.constrains` 和 `_sql_constraints`

### 安全规划
- 访问权限：ir.model.access.csv 配置
- 记录规则：ir.rule 多用户数据隔离
- 安全组：res.groups 层级配置
- 权限最小化原则

### 视图规划
- Tree 视图：列表显示
- Form 视图：表单编辑
- Kanban 视图：看板视图
- Pivot/Graph：数据分析
- 搜索视图：筛选和分组

## 使用示例

```
用户: /plan 需要为销售订单添加自定义字段，并在报表中显示

Agent (planner):
# Odoo 19 实施计划：销售订单自定义字段扩展

## 需求重述
- 为 sale.order 模型添加自定义字段
- 在销售订单表单中显示这些字段
- 在销售报表（Pivot/Graph）中使用这些字段
- 确保字段可翻译
- 考虑多公司场景

## 实施阶段

### Phase 1: 模型扩展
- 文件: models/sale_order.py
- 继承: sale.order
- 添加字段: custom_field1, custom_field2, custom_date
- 添加计算字段（如果需要）
- 添加约束
- Risk: Low

### Phase 2: 视图更新
- 文件: views/sale_order_views.xml
- 扩展 sale.order.form 视图
- 在表单中添加新字段
- 更新搜索视图以支持新字段筛选
- Risk: Low

### Phase 3: 报表更新
- 文件: views/sale_order_views.xml
- 扩展 Pivot 视图以包含新字段作为度量
- 扩展 Graph 视图以支持新字段分组
- Risk: Low

### Phase 4: 安全配置
- 文件: security/security.xml
- 确保访问权限正确继承
- 添加记录规则（如果需要）
- Risk: HIGH - 安全关键

### Phase 5: 测试
- 文件: tests/test_sale_order_extension.py
- 测试新字段创建和更新
- 测试计算字段
- 测试约束
- 测试多公司场景
- Risk: Low

## 依赖
- sale 模块（需要继承 sale.order）
- web 模块（视图支持）

## 风险
- MEDIUM: 如果字段在现有订单中有数据，需要数据迁移
- LOW: 视图扩展可能影响自定义视图
- LOW: 报表性能可能受影响（取决于数据量）

## 估算复杂度: LOW
- 模型扩展: 1-2 小时
- 视图更新: 1-2 小时
- 报表更新: 1-2 小时
- 安全配置: 30 分钟
- 测试: 2-3 小时
- 总计: 5.5-9.5 小时

**等待确认**: 继续执行此计划？(yes/no/modify)
```

## 重要提示

**关键**: planner agent **不会** 编写任何代码，直到您明确用 "yes" 或 "proceed" 或类似的肯定回复确认计划。

如果您想要更改，请回复：
- "modify: [您的更改]"
- "different approach: [替代方案]"
- "skip phase 2 and do phase 3 first"

## 与其他命令的集成

规划后：
- 使用 `/tdd` 以测试驱动开发方式实施
- 如果出现构建错误，使用 `/code-review` 审查代码
- 完成实施后使用 `/code-review` 进行审查

## 相关 Agent

此命令调用位于以下位置的 `planner` agent：
`~/.claude/agents/planner.md`

## Odoo 19 最佳实践

1. **遵循 Odoo 约定**：使用标准模块结构和命名模式
2. **安全优先**：始终规划访问权限和记录规则
3. **使用继承**：尽可能扩展现有模型
4. **规划升级**：考虑现有安装的数据迁移
5. **早期测试**：规划与模型测试并行的 UI 测试
6. **文档完整**：为类和方法添加 docstrings
7. **多公司支持**：考虑是否需要多公司支持
8. **多语言支持**：正确规划可翻译字符串

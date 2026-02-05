---
description: Odoo 19 测试驱动开发工作流命令。首先定义接口、生成测试，然后实现最小代码以通过测试。确保 80%+ 测试覆盖率。
---

# Odoo 19 TDD 命令

此命令调用 **tdd-guide** agent 以强制执行 Odoo 19 的测试驱动开发方法论。

## 命令功能

1. **定义接口** - 首先定义模型/方法的输入输出
2. **先编写测试** - 编写失败的测试（RED）
3. **实现最小代码** - 编写刚好使测试通过的代码（GREEN）
4. **重构** - 改进代码同时保持测试通过（REFACTOR）
5. **验证覆盖率** - 确保 80%+ 测试覆盖率

## 使用场景

当以下情况时使用 `/tdd`：
- 实现新的 Odoo 模型或方法
- 添加新的 Odoo 视图或控制器
- 修复 bug（先编写重现 bug 的测试）
- 重构现有 Odoo 代码
- 构建关键业务逻辑

## 工作原理

tdd-guide agent 将执行以下操作：

1. **定义接口** 用于输入输出
2. **编写会失败的测试**（因为代码还不存在）
3. **运行测试** 并验证因正确原因失败
4. **编写最小实现** 使测试通过
5. **运行测试** 并验证通过
6. **重构** 代码同时保持测试通过
7. **检查覆盖率** 如果低于 80% 则添加更多测试

## Odoo 19 TDD 循环

```
RED (红) → GREEN (绿) → REFACTOR (重构) → 重复

RED:      编写失败的测试
GREEN:    编写最小代码通过测试
REFACTOR: 改进代码，保持测试通过
REPEAT:   下一个功能/场景
```

## Odoo 19 测试类型

### 1. TransactionCase - 模型测试

用于测试 Odoo 模型方法、字段、约束：

```python
from odoo.tests import TransactionCase, tagged

@tagged('post_install', '-at_install')
class TestMyModel(TransactionCase):
    """测试 MyModel 的方法和约束"""

    def setUp(self):
        super(TestMyModel, self).setUp()
        self.Model = self.env['my.model']

    def test_create_record(self):
        """测试创建记录"""
        record = self.Model.create({
            'name': 'Test Record',
            'value': 100,
        })
        self.assertTrue(record.id)
        self.assertEqual(record.name, 'Test Record')

    def test_computed_field(self):
        """测试计算字段"""
        record = self.Model.create({
            'name': 'Test',
            'value1': 10,
            'value2': 20,
        })
        self.assertEqual(record.compute_total, 30)
```

### 2. HttpCase - 控制器测试

用于测试 HTTP 路由和控制器：

```python
@tagged('post_install', '-at_install')
class TestMyController(HttpCase):
    """测试 MyController HTTP 端点"""

    def test_index_page_loads(self):
        """测试主页面加载"""
        response = self.url_open('/my/module')
        self.assertEqual(response.status_code, 200)
        self.assertIn('My Module', response.text)
```

### 3. 安全测试

测试访问权限和记录规则：

```python
@tagged('post_install', '-at_install')
class TestSecurity(TransactionCase):
    """测试安全配置"""

    def test_user_can_read_own_records(self):
        """测试用户可以读取自己的记录"""
        user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'test@example.com',
        })
        record = self.env['my.model'].sudo(user).create({'name': 'Test'})

        # 用户应该能读取自己的记录
        user_records = self.env['my.model'].with_user(user).search([])
        self.assertIn(record.id, user_records.ids)
```

## 使用示例

```
用户: /tdd 需要为销售订单添加一个计算折扣的方法

Agent (tdd-guide):
# Odoo 19 TDD 会话：销售订单折扣计算器

## 步骤 1: 定义接口（脚手架）

```python
# models/sale_order.py
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def calculate_discount(self, discount_percent):
        """根据百分比计算折扣金额

        Args:
            discount_percent: 折扣百分比 (0-100)

        Returns:
            float: 折扣金额
        """
        # TODO: 实现
        raise NotImplementedError('Not implemented')
```

## 步骤 2: 编写失败的测试（RED）

```python
# tests/test_sale_order_discount.py
from odoo.tests import TransactionCase, tagged

@tagged('post_install', '-at_install')
class TestSaleOrderDiscount(TransactionCase):
    """测试销售订单折扣计算"""

    def setUp(self):
        super(TestSaleOrderDiscount, self).setUp()
        self.partner = self.env['res.partner'].create({'name': 'Test Partner'})
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100,
        })

    def test_calculate_discount_10_percent(self):
        """测试 10% 折扣计算"""
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [
                (0, 0, {
                    'product_id': self.product.id,
                    'product_uom_qty': 1,
                    'price_unit': 100,
                }),
            ],
        })
        self.assertEqual(order.amount_untaxed, 100.0)

        discount = order.calculate_discount(10)
        self.assertEqual(discount, 10.0)

    def test_calculate_discount_zero_percent(self):
        """测试 0% 折扣计算"""
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [
                (0, 0, {
                    'product_id': self.product.id,
                    'product_uom_qty': 2,
                    'price_unit': 50,
                }),
            ],
        })

        discount = order.calculate_discount(0)
        self.assertEqual(discount, 0.0)

    def test_calculate_discount_invalid_percent(self):
        """测试无效折扣百分比"""
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [
                (0, 0, {
                    'product_id': self.product.id,
                    'product_uom_qty': 1,
                    'price_unit': 100,
                }),
            ],
        })

        with self.assertRaises(ValueError):
            order.calculate_discount(150)  # 超过 100%

        with self.assertRaises(ValueError):
            order.calculate_discount(-10)  # 负值
```

## 步骤 3: 运行测试 - 验证失败

```bash
odoo -d test_db --test-enable --test-tags=test_sale_order_discount --stop-after-init

FAIL tests/test_sale_order_discount.py
  ✕ test_calculate_discount_10_percent (2 ms)
    NotImplementedError: Not implemented

3 tests failed, 0 passed
```

测试按预期失败。准备实现。

## 步骤 4: 实现最小代码（GREEN）

```python
# models/sale_order.py
def calculate_discount(self, discount_percent):
    """根据百分比计算折扣金额"""
    self.ensure_one()

    # 验证折扣百分比
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError(_('Discount percentage must be between 0 and 100'))

    # 计算折扣
    return self.amount_untaxed * (discount_percent / 100)
```

## 步骤 5: 运行测试 - 验证通过

```bash
odoo -d test_db --test-enable --test-tags=test_sale_order_discount --stop-after-init

PASS tests/test_sale_order_discount.py
  ✓ test_calculate_discount_10_percent (3 ms)
  ✓ test_calculate_discount_zero_percent (2 ms)
  ✓ test_calculate_discount_invalid_percent (1 ms)

3 tests passed
```

所有测试通过！

## 步骤 6: 重构（IMPROVE）

```python
# models/sale_order.py - 添加更多场景和边界测试
def calculate_discount(self, discount_percent, limit_percent=None):
    """根据百分比计算折扣金额

    Args:
        discount_percent: 折扣百分比 (0-100)
        limit_percent: 最大允许折扣百分比（如果设置）

    Returns:
        float: 折扣金额

    Raises:
        ValueError: 如果折扣百分比无效
    """
    self.ensure_one()

    # 验证折扣百分比
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError(_('Discount percentage must be between 0 and 100'))

    # 应用最大折扣限制（如果设置）
    if limit_percent and discount_percent > limit_percent:
        discount_percent = limit_percent

    # 计算折扣
    return self.amount_untaxed * (discount_percent / 100)
```

## 步骤 7: 添加更多测试并验证通过

```python
def test_calculate_discount_with_limit(self):
    """测试带限制的折扣计算"""
    order = self.env['sale.order'].create({
        'partner_id': self.partner.id,
        'order_line': [
            (0, 0, {
                'product_id': self.product.id,
                'product_uom_qty': 1,
                'price_unit': 100,
            }),
        ],
    })

    # 尝试 50% 折扣但限制为 20%
    discount = order.calculate_discount(50, limit_percent=20)
    self.assertEqual(discount, 20.0)
```

## 步骤 8: 检查覆盖率

```bash
# Odoo 覆盖率
odoo -d test_db --test-enable --test-tags=test_sale_order_discount --stop-after-init

# 检查覆盖率报告
# 覆盖率应为 80%+（生产代码）

File           | % Stmts | % Branch | % Funcs | % Lines
---------------|---------|----------|---------|--------
sale_order.py  |   100   |   100    |   100   |   100

覆盖率: 100% ✅（目标: 80%）

TDD 会话完成！
```

## Odoo 19 TDD 最佳实践

**应该做:**
- ✅ 先编写测试，再编写实现
- ✅ 在实施前运行测试并验证失败
- ✅ 编写最小代码使测试通过
- ✅ 测试通过后进行重构
- ✅ 添加边缘情况和错误场景
- ✅ 目标 80%+ 覆盖率（关键代码 100%）

**不应该做:**
- ❌ 在测试之前编写实现
- ❌ 每次更改后跳过运行测试
- ❌ 一次编写太多代码
- ❌ 忽略失败的测试
- ❌ 测试实现细节（测试行为）
- ❌ 模拟所有内容（更喜欢集成测试）

## 必须包含的测试类型

**单元测试**（函数级别）:
- 正常路径场景
- 边缘情况（空、null、最大值）
- 错误条件
- 边界值

**集成测试**（组件级别）:
- ORM 操作
- 数据库操作
- 外部服务调用
- 带钩子的模型

**安全测试**（必须）:
- 访问权限
- 记录规则
- 用户组访问

## Odoo 19 覆盖率要求

- **80% 最低** 所有代码
- **100% 必须** 对于：
  - 财务计算
  - 认证逻辑
  - 安全关键代码
  - 核心业务逻辑

## 重要提示

**强制**: 测试必须先于实现编写。TDD 循环是：

1. **RED** - 编写失败的测试
2. **GREEN** - 实现以通过测试
3. **REFACTOR** - 改进代码

永远不要跳过 RED 阶段。永远不要在测试之前编写代码。

## 与其他命令的集成

- 使用 `/plan` 首先了解要构建什么
- 使用 `/tdd` 以测试驱动方式实施
- 使用 `/code-review` 审查实施
- 使用 `/security-review` 进行安全审查

## 相关 Agent

此命令调用位于以下位置的 `tdd-guide` agent：
`~/.claude/agents/tdd-guide.md`

## Odoo 19 测试装饰器

```python
from odoo.tests import common, tagged

# 标记测试
@tagged('post_install', '-at_install')
class MyTests(TransactionCase):
    """在模块安装后运行（带演示数据）"""

@tagged('standard')
class MyTests(TransactionCase):
    """默认 - 在安装前运行（无演示数据）"""
```

## 记住

没有测试的 Odoo 代码。在 Odoo 中测试不是可选的 - 它们确保模块在升级期间工作，保持安全性，并在到达生产环境之前捕获回归。

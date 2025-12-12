招商银行 PDF 流水 → CSV 转换工具

一个用于将 **招商银行电子回单（PDF 格式）自动转换为结构化 CSV 文件**的小工具。
 支持 **批量处理**，CLI / 拖放均可使用。

------

## 功能

- **自动识别交易行**（基于日期正则，适配绝大多数格式）
- **清洗无效行、英文表头、杂项内容**

------

## 用法

### 使用 Python 运行

```
python main.py pdf路径1 pdf路径2 ...
```

------

### 使用打包后的可执行文件（Windows）

#### 方法 1：拖放运行

将一个或多个 PDF 文件拖放到 `release.exe` 上即可。

#### 方法 2：命令行运行

```
release.exe pdf路径1 pdf路径2 ...
```

------

## 从源代码打包

### 使用 PyInstaller：

```
pyinstaller main.py --onefile
```

### 使用 Nuitka：

```
nuitka main.py --onefile --standalone
```

------

## 📄 输出格式（CSV 字段）

| 字段名       | 含义     |
| ------------ | -------- |
| date         | 记账日期 |
| currency     | 币种     |
| amount       | 交易金额 |
| balance      | 联机余额 |
| summary      | 交易摘要 |
| counterparty | 对手信息 |

注意：
 如果原始行中字段不足 6 个，则自动填补空值；若字段过多，会将尾部合并为对手信息。

------

## TODO

-  **拼接跨行被截断的商户名称 / 对手信息**


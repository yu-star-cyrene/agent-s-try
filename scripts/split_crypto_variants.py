from __future__ import annotations

from pathlib import Path
import runpy
import shutil


ROOTS = [
    Path("tmp_crypto_handbook"),
    Path(r"C:\Users\yu\Desktop\密码"),
]

SOURCE_INTRO_BASE = (
    "这份资料基于 `C:\\Users\\yu\\Downloads\\2.txt` 中的《CTF Crypto 常见题型总结》整理，并强化成“看到什么数据/提示时该想到什么题型”的速查笔记。"
)
SOURCE_INTRO_MERGED = (
    "这份资料基于 `C:\\Users\\yu\\Downloads\\2.txt` 的《CTF Crypto 常见题型总结》与 "
    "`C:\\Users\\yu\\Downloads\\1.txt` 的《CTF Crypto 变体题型大全》共同整理，并强化成"
    "“看到什么数据/提示时该想到什么题型、遇到哪些伪装时该往哪类靠”的速查笔记。"
)
SECTION_TITLE = "## 高频变体与伪装方式"
INSERT_BEFORE = "## 实战里建议怎么入手"


BASE_TOPICS = [
    {
        "base_folder": "01_古典密码",
        "variant_folder": "19_古典密码变体",
        "base_title": "古典密码",
        "variant_title": "古典密码变体",
        "base_desc": "以字母替换、位置重排、查表映射为主的入门型 Crypto 题。",
        "variant_desc": "已经确定是古典密码后，用来继续区分位移、重排、A/B 映射、图形和键盘伪装等分支。",
    },
    {
        "base_folder": "02_编码与变换",
        "variant_folder": "20_编码与变换变体",
        "base_title": "编码与变换",
        "variant_title": "编码与变换变体",
        "base_desc": "更像是数据表示层的变换，不一定是真正的加密，但在 CTF 里经常作为第一层壳。",
        "variant_desc": "专门整理 Base、转义、字节序、多层套娃这些“看着像编码但藏了额外花样”的出法。",
    },
    {
        "base_folder": "03_XOR异或",
        "variant_folder": "21_XOR异或变体",
        "base_title": "XOR 异或",
        "variant_title": "XOR 异或变体",
        "base_desc": "CTF 里最高频的基础套路之一，既能单独出题，也常被放进多层套娃里。",
        "variant_desc": "聚焦单字节、多字节、已知明文、双密文同 key、文件头利用等具体异或出法。",
    },
    {
        "base_folder": "04_流密码",
        "variant_folder": "22_流密码变体",
        "base_title": "流密码",
        "variant_title": "流密码变体",
        "base_desc": "把密钥流逐字节与明文异或的加密方式，题目常从 keystream、LFSR、RC4、ChaCha 或弱随机源下手。",
        "variant_desc": "专门归纳 RC4、ChaCha、LFSR、BM、多寄存器组合和自定义 PRNG 这类流密码分支。",
    },
    {
        "base_folder": "05_分组密码",
        "variant_folder": "23_分组密码变体",
        "base_title": "分组密码",
        "variant_title": "分组密码变体",
        "base_desc": "以 AES、DES、TEA、Feistel 为主，识别重点通常在模式、IV、padding、oracle 和重复块。",
        "variant_desc": "用来细分 ECB/CBC/CTR/GCM、3DES MITM、TEA、白盒和实现失误这些常见分支。",
    },
    {
        "base_folder": "06_RSA",
        "variant_folder": "24_RSA变体",
        "base_title": "RSA",
        "variant_title": "RSA 变体",
        "base_desc": "CTF Crypto 的核心重灾区，真正考点几乎都来自参数弱点和额外泄露。",
        "variant_desc": "单独收纳高低位泄露、Wiener、Boneh-Durfee、Rabin、oracle、批量 gcd、组合包装等细分套路。",
    },
    {
        "base_folder": "07_ECC椭圆曲线",
        "variant_folder": "25_ECC椭圆曲线变体",
        "base_title": "ECC 椭圆曲线",
        "variant_title": "ECC 椭圆曲线变体",
        "base_desc": "围绕椭圆曲线群运算、离散对数、ECDH/ECDSA 的题型，核心是识别曲线参数和群结构是否有弱点。",
        "variant_desc": "进一步拆成光滑阶、小阶子群、异常曲线、奇异曲线、MOV 以及 ECDSA nonce 相关漏洞。",
    },
    {
        "base_folder": "08_格密码与LLL",
        "variant_folder": "26_格密码与LLL变体",
        "base_title": "格密码与 LLL",
        "variant_title": "格密码与 LLL 变体",
        "base_desc": "题目经常伪装成背包、小根、部分泄露、近似方程，本质上是在考格构造和约化。",
        "variant_desc": "把 subset sum、Coppersmith、HNP、NTRU、LWE/RLWE、CVP/SVP 这些变体单独收纳。",
    },
    {
        "base_folder": "09_哈希与MAC",
        "variant_folder": "27_哈希与MAC变体",
        "base_title": "哈希与 MAC",
        "variant_title": "哈希与 MAC 变体",
        "base_desc": "重点不是反推出原文，而是识别哈希用途、是否可爆破、是否存在长度扩展或错误的签名/比较方式。",
        "variant_desc": "单独区分弱口令爆破、长度扩展、HMAC 错用、Timing Attack、碰撞和 CRC32 伪造。",
    },
    {
        "base_folder": "10_随机数预测",
        "variant_folder": "28_随机数预测变体",
        "base_title": "随机数预测",
        "variant_title": "随机数预测变体",
        "base_desc": "题目本质不是密码学本身，而是生成密钥、nonce、shuffle 顺序的随机源太弱。",
        "variant_desc": "用来细分 MT19937、time seed、短字符串 seed、LCG、Java Random、C rand、xorshift 等具体弱源。",
    },
    {
        "base_folder": "11_数学数论",
        "variant_folder": "29_数学数论变体",
        "base_title": "数学数论",
        "variant_title": "数学数论变体",
        "base_desc": "很多 Crypto 题表面像算法，底层其实就是模运算、逆元、CRT、DLP、二次剩余这些数论工具题。",
        "variant_desc": "把 CRT、离散对数、二次剩余、连分数、Pell、多项式环等更细的数论分支独立出来。",
    },
    {
        "base_folder": "12_协议类",
        "variant_folder": "30_协议类变体",
        "base_title": "协议类",
        "variant_title": "协议类变体",
        "base_desc": "考点常出现在密钥交换、身份认证、参数协商和签名验证流程里，重点是看协议有没有把密码学原语用对。",
        "variant_desc": "专门整理 DH 弱参数、MITM、SRP 边界值、JWT 和 Cookie/区块链签名这类协议层变体。",
    },
    {
        "base_folder": "13_签名算法",
        "variant_folder": "31_签名算法变体",
        "base_title": "签名算法",
        "variant_title": "签名算法变体",
        "base_desc": "重点是识别 nonce、padding、验证规则是否安全，而不是怎么把签名算法算一遍。",
        "variant_desc": "单独收纳 DSA/ECDSA nonce 重用、部分泄露、Schnorr/EdDSA 分支、RSA 签名伪造和可塑性。",
    },
    {
        "base_folder": "14_Padding",
        "variant_folder": "32_Padding变体",
        "base_title": "Padding",
        "variant_title": "Padding 变体",
        "base_desc": "Padding 本身不是算法，但它经常成为 AES-CBC、RSA PKCS#1 v1.5 这类题真正能打进去的缺口。",
        "variant_desc": "把 PKCS#7、CBC padding oracle、PKCS#1 v1.5、OAEP 错误使用这些方向单独归一类。",
    },
    {
        "base_folder": "15_图片音频文件混合Crypto",
        "variant_folder": "33_图片音频文件混合Crypto变体",
        "base_title": "图片 / 音频 / 文件混合 Crypto",
        "variant_title": "图片 / 音频 / 文件混合 Crypto 变体",
        "base_desc": "题目载体看起来像 Misc，但真正突破点在于你需要先从媒体里抽出可被 Crypto 处理的数据。",
        "variant_desc": "专门整理像素转 bit、频谱图、隐藏对象、二维码链路、文件头利用等混合载体出法。",
    },
    {
        "base_folder": "16_自定义密码",
        "variant_folder": "34_自定义密码变体",
        "base_title": "自定义密码算法",
        "variant_title": "自定义密码变体",
        "base_desc": "作者自己写的加密往往不安全，关键是把每一步拆开，看它到底是线性的、可逆的、可枚举的，还是能转成方程。",
        "variant_desc": "把可逆运算、置换、shuffle、矩阵、GF(2) 线性系统、Z3 和魔改分组密码的分支单独展开。",
    },
    {
        "base_folder": "17_脑洞类Crypto",
        "variant_folder": "35_脑洞类Crypto变体",
        "base_title": "脑洞类 Crypto",
        "variant_title": "脑洞类 Crypto 变体",
        "base_desc": "这类题不一定强依赖数学，而是把提示藏在标题、文件名、排版、首字母、藏头等地方。",
        "variant_desc": "把题名伪装、文件名提示、结构性提示、假 Crypto 真编码和混合附件提示独立出来。",
    },
    {
        "base_folder": "18_组合套娃",
        "variant_folder": "36_组合套娃变体",
        "base_title": "组合套娃",
        "variant_title": "组合套娃变体",
        "base_desc": "比赛里很少只考一层，真正高频的是多种简单方法串联：先提取，再解码，再做 XOR 或 AES。",
        "variant_desc": "把 RSA+AES、随机数+AES、LFSR+XOR、图片+Bacon+Base64、区块链+ECDSA 等典型链路单列出来。",
    },
]


def load_variants() -> dict[str, list[str]]:
    data = runpy.run_path(str(Path("scripts") / "integrate_crypto_variants.py"))
    return data["VARIANTS"]


def strip_variant_section(text: str) -> str:
    text = text.replace(SOURCE_INTRO_MERGED, SOURCE_INTRO_BASE)
    if SECTION_TITLE in text and INSERT_BEFORE in text:
        before, rest = text.split(SECTION_TITLE, 1)
        _, after = rest.split(INSERT_BEFORE, 1)
        text = before.rstrip() + "\n\n" + INSERT_BEFORE + after
    return text


def build_variant_readme(meta: dict[str, str], bullets: list[str]) -> str:
    lines = [
        f"# {meta['variant_title']}",
        "",
        "这份资料主要基于 `C:\\Users\\yu\\Downloads\\1.txt` 中的《CTF Crypto 变体题型大全》整理，作用不是重新教你认基础题型，而是在你已经锁定大方向之后，继续帮你分流到更具体的弱点、泄露、交互或伪装出法。",
        "",
        "## 题型表述",
        "",
        meta["variant_desc"],
        "",
        "## 和基础题型的区别",
        "",
        f"- 基础题型目录：`{meta['base_folder']}`，负责先判断“大方向是不是这一类”。",
        f"- 当前变体目录：`{meta['variant_folder']}`，负责继续判断“这一类里到底是哪种细分出题方式”。",
        "- 如果你已经知道算法名字，但普通模板走不通，就应该立刻来看对应的变体目录。",
        "",
        "## 什么时候该切到变体思路",
        "",
        "- 你已经能确定大方向，但基础模板无法直接落地，说明题目多半在考弱参数、泄露、oracle、实现错误或组合包装。",
        "- 题目除了核心密文，还多给了额外参数、文件格式、服务端交互、已知结构、奇怪提示词或边界输入。",
        "- 题名里出现 `baby`、`leak`、`oracle`、`next_prime`、`time seed`、`nonce reuse`、`fixed iv` 等词时，往往不是基础版。",
        "- 同一种算法如果被拆成好几层附件、脚本、交互服务，通常就已经进入变体范围了。",
        "",
        "## 这一类高频变体",
        "",
    ]
    lines.extend(f"- {bullet}" for bullet in bullets)
    lines.extend(
        [
            "",
            "## 实战里建议怎么用",
            "",
            f"- 先回基础目录 `{meta['base_folder']}` 确认自己没有认错大方向。",
            "- 再拿这份变体清单去对照题目里的额外参数、提示词、文件名、返回信息和交互行为。",
            "- 一旦能把题目归到某个具体变体，再去改同目录下的 `example.py`，把它扩成适合当前题目的脚本。",
            "",
            "## 配套示例脚本说明",
            "",
            "这里的 `example.py` 先沿用对应基础题型的起手模板，作用是让你把主框架搭起来。真正遇到具体变体时，请根据本页的细分方向继续补上对应攻击步骤。",
            "",
        ]
    )
    return "\n".join(lines)


def rebuild_index(root: Path) -> None:
    lines = [
        "# CTF Crypto 题型资料包",
        "",
        "整理来源：",
        "",
        "- 基础题型：`C:\\Users\\yu\\Downloads\\2.txt`",
        "- 变体题型：`C:\\Users\\yu\\Downloads\\1.txt`",
        "",
        "这个目录现在分成两层：",
        "",
        "- `01-18`：基础题型，先帮你判断大方向。",
        "- `19-36`：对应的变体题型，在已经确定大方向后，继续判断具体弱点、泄露、oracle、伪装和组合包装。",
        "",
        "每个题型文件夹里都有两份内容：",
        "",
        "- `README.md`：讲清楚题型表述、识别信号、什么时候该想到它。",
        "- `example.py`：放一个可以直接对照改写的起手脚本。",
        "",
        "## 基础题型",
        "",
    ]
    for item in BASE_TOPICS:
        lines.append(f"- `{item['base_folder']}`：{item['base_title']}。{item['base_desc']}")
    lines.extend(["", "## 变体题型", ""])
    for item in BASE_TOPICS:
        lines.append(f"- `{item['variant_folder']}`：对应 `{item['base_folder']}`。{item['variant_desc']}")
    lines.extend(
        [
            "",
            "## 建议使用方式",
            "",
            "- 先看基础题型目录，先把题目归到大方向。",
            "- 大方向确定后，如果普通模板不通，再切到对应的变体目录继续分流。",
            "- 真正写脚本时，先从 `example.py` 起手，再按题面补上具体变体逻辑。",
            "- 组合题优先同时参考基础目录 `18_组合套娃` 和变体目录 `36_组合套娃变体`。",
            "",
        ]
    )
    (root / "00_总索引.md").write_text("\n".join(lines), encoding="utf-8")


def update_root(root: Path, variants: dict[str, list[str]]) -> None:
    if not root.exists():
        return

    for item in BASE_TOPICS:
        base_readme = root / item["base_folder"] / "README.md"
        if base_readme.exists():
            text = base_readme.read_text(encoding="utf-8")
            base_readme.write_text(strip_variant_section(text), encoding="utf-8")

        variant_dir = root / item["variant_folder"]
        variant_dir.mkdir(parents=True, exist_ok=True)
        bullets = variants[item["base_folder"]]
        variant_readme = build_variant_readme(item, bullets)
        (variant_dir / "README.md").write_text(variant_readme, encoding="utf-8")

        base_example = root / item["base_folder"] / "example.py"
        if base_example.exists():
            shutil.copyfile(base_example, variant_dir / "example.py")

    rebuild_index(root)


def main() -> None:
    variants = load_variants()
    for root in ROOTS:
        update_root(root, variants)
        print(f"split variants under {root}")


if __name__ == "__main__":
    main()

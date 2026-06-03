from __future__ import annotations

from pathlib import Path


SOURCE_INTRO_OLD = (
    "这份资料基于 `C:\\Users\\yu\\Downloads\\2.txt` 中的《CTF Crypto 常见题型总结》整理，并强化成“看到什么数据/提示时该想到什么题型”的速查笔记。"
)
SOURCE_INTRO_NEW = (
    "这份资料基于 `C:\\Users\\yu\\Downloads\\2.txt` 的《CTF Crypto 常见题型总结》与 "
    "`C:\\Users\\yu\\Downloads\\1.txt` 的《CTF Crypto 变体题型大全》共同整理，并强化成"
    "“看到什么数据/提示时该想到什么题型、遇到哪些伪装时该往哪类靠”的速查笔记。"
)

SECTION_TITLE = "## 高频变体与伪装方式"
INSERT_BEFORE = "## 实战里建议怎么入手"

ROOTS = [
    Path("tmp_crypto_handbook"),
    Path(r"C:\Users\yu\Desktop\密码"),
]

VARIANTS: dict[str, list[str]] = {
    "01_古典密码": [
        "凯撒变体：正移、反移、大小写分开处理、字母表顺序被改、先反转再位移、和 ASCII 偏移混在一起。",
        "仿射变体：直接给 `a,b`，或者只在题名里写 `affine`、`ax+b mod 26`，本质上还是枚举互素的 `a`。",
        "维吉尼亚变体：已知 key 直接解、短 key 爆破、Kasiski、重合指数 IC、关键词里夹杂非字母字符。",
        "栅栏变体：行数未知、W 型方向不同、先写后读和先读后写混淆、需要枚举行数或轨迹。",
        "列置换变体：key 已知、列顺序未知、补齐字符扰动、按行填充还是按列填充需要先分清。",
        "培根变体：大小写、粗细字体、黑白像素、0/1、`a/b`、两种符号分别映射 A/B。",
        "摩斯变体：`.`/`-` 被替换成 `0/1`、空格丢失、整体倒序、点横反转、音频长短音映射。",
        "键盘与图形变体：QWERTY 位移、键盘坐标、手机 T9、盲文、猪圈、跳舞小人都属于高频伪装。",
    ],
    "02_编码与变换": [
        "Base 系列变体：除了 Base64、Base32、Hex，还要警惕 Base58、Base85、URL-safe Base64、缺 padding 的 Base64。",
        "URL / Unicode / HTML 实体经常连着套，比如 `%66%6c` 解完后又得到 `\\u0066` 或 `&#102;`。",
        "ASCII 数字变体：十进制数字串可能用空格、逗号、换行分隔，先拆组再转字符。",
        "二进制 / 八进制 / 十六进制变体：同一串数据可能要按 8 位、7 位、5 位分组，或者先 reverse 再解。",
        "大小端变体：看起来像正常十六进制，但字节序反了，尤其常见于整数字段和文件头。",
        "多层套娃变体：`hex -> ascii -> base64`、`base64 -> url -> rot13` 这种分层包装非常常见。",
    ],
    "03_XOR异或": [
        "单字节 XOR：短密文、单条 hex、结果应为可打印文本时先枚举 `0~255`。",
        "多字节循环 XOR：key 较短、密文较长、可按列拆分成多个单字节 XOR 子问题。",
        "已知明文攻击：已知 `flag{`、PNG 头、`PK`、`%PDF` 之类前缀时，可以直接反推出 key 或 keystream。",
        "Two-time pad：两份密文共用同一 key 时，`c1 ^ c2 = m1 ^ m2`，结构信息会直接漏出来。",
        "图片 / 文件 XOR：不是只盯文本，图片、压缩包、PE 文件头都能拿来做已知明文。",
        "套娃变体：外层是 Hex/Base64，里层才是 XOR，或者 XOR 完以后还要继续解码下一层。",
    ],
    "04_流密码": [
        "RC4 / Rabbit / ChaCha20 / Salsa20：标准流密码题通常不爆算法本身，而是打 key、nonce、state 复用。",
        "ChaCha20 / Salsa20 / CTR 类似变体里，`nonce` 重用最危险，看到重复 nonce 就要高度警惕。",
        "LFSR 变体：题面会给反馈多项式、寄存器抽头、位流输出，目标通常是恢复初始状态。",
        "Berlekamp-Massey 变体：只给足够长的输出位流，要求你直接求最短 LFSR。",
        "多 LFSR 组合：多个寄存器异或、相加或做布尔组合，比单个 LFSR 多了一层拆分。",
        "自定义 PRNG 流密码：作者自己写 `state = f(state)` 再拿输出去 XOR，本质还是先恢复状态再解密。",
    ],
    "05_分组密码": [
        "ECB 变体：重复块识别、byte-at-a-time、cut-and-paste 都是高频题型。",
        "CBC 变体：bit flipping、padding oracle、IV 可控、IV 固定，这四种出现率都很高。",
        "CTR 变体：本质更像流密码，常见的是 nonce 重用和 bit flipping。",
        "GCM 变体：重点不是 AES 本身，而是 `nonce` 重用后导致认证和机密性一起出问题。",
        "CFB / OFB 也会出题，但通常思路仍是 keystream 或状态复用，而不是正面硬解。",
        "实现类变体：密钥长度填错、弱口令派生 key、padding 处理错误、AES + 压缩侧信道、白盒 / 魔改 AES。",
        "同目录也要顺手联想到 DES 弱密钥、3DES meet-in-the-middle、TEA/XTEA/XXTEA、自定义 Feistel。",
    ],
    "06_RSA": [
        "直接分解变体：`baby_rsa`、`n` 太小、FactorDB / yafu 一把过，仍然是最常见入口。",
        "结构分解变体：`p≈q`、`q = next_prime(p+k)`、`n` 是质数幂、`n` 有重复因子、多素数 RSA、`p/q` 不是真素数。",
        "部分泄露变体：`p/q` 高位、低位、中间位、共同高位、`n` 或 `phi` 不完整，都可能转成小根或格问题。",
        "关系泄露变体：`p+q`、`p-q`、`p xor q`、`p&q`、`p|q` 以及这些量的组合，核心是构造 `p+q` 或按 bit DFS。",
        "私钥泄露变体：`phi`、`d`、`d` 高低位、`dp`、`dq`、`qinv` 泄露都非常高频。",
        "小私钥变体：Wiener、Boneh-Durfee、partial key exposure，看到 `d` 很小就别再按普通解法磨了。",
        "小指数变体：`e=3/5` 且明文小、`c + k*n = m^e`、Hastad 广播、Common Modulus、`e` 与 `phi` 不互素。",
        "Rabin / `e=2` 变体：通常要在 `mod p` 和 `mod q` 下开平方，再用 CRT 组合候选解。",
        "多公钥变体：多个 `n` 共因子、批量公钥 gcd、同一明文或相关明文都要警惕。",
        "明文结构变体：已知前缀、已知后缀、明文很小、明文格式可预测，往往能直接减少未知量。",
        "组合包装变体：RSA 外面套 Base 编码、RSA 只负责解出 AES key、私钥文件加密、从公钥/证书提取 `n,e`。",
        "交互与伪造变体：signature forgery、parity oracle、LSB/MSB oracle、padding oracle、decryption oracle、同态变体、`e=1`。",
    ],
    "07_ECC椭圆曲线": [
        "ECDH 变体：私钥过小可枚举，或者密钥交换落在小群里导致共享密钥范围很小。",
        "群阶光滑变体：曲线阶或子群阶可分解得很碎时，优先想到 Pohlig-Hellman。",
        "小阶子群攻击：题目允许你送点进去时，要检查对方有没有验证点阶和曲线归属。",
        "异常 / 奇异曲线变体：`anomalous curve`、`singular curve` 往往意味着不能再按普通 ECC 安全性理解。",
        "MOV Attack：题目若提 embedding degree、pairing 或把 ECC 转到有限域乘法群，就是这个方向。",
        "ECDSA 变体：nonce 重用、nonce 部分泄露、`random.seed(...)` 生成 nonce 都会直接泄露私钥。",
        "同类签名题也要顺手联想到 EdDSA / Schnorr 的 nonce 问题，虽然公式不同，漏洞思路很像。",
    ],
    "08_格密码与LLL": [
        "背包密码 / 子集和：最典型的格题外观，先判断是不是超递增，再决定 LLL 还是 meet-in-the-middle。",
        "Coppersmith 小根：只要看到“未知部分很小”“高位已知”“低位已知”，就要往 small roots 靠。",
        "HNP：ECDSA/DSA nonce 的部分泄露、本质上经常转成 Hidden Number Problem。",
        "NTRU：题面会出现多项式环、小模数和格结构，别再按 RSA 那套想。",
        "LWE / RLWE：给很多带噪线性关系时，要警惕这是学习误差类题目。",
        "CVP / SVP 变体：题目如果直接讲最近向量、短向量、近似整数解，就是在暗示格约化目标。",
    ],
    "09_哈希与MAC": [
        "简单 hash 爆破：短明文、字典词、弱口令、题面暗示词典来源时，优先爆破而不是瞎逆向。",
        "弱密码 hash：MD5/SHA1/SHA256 本身没坏，但人类口令太弱时仍然是一秒钟题。",
        "长度扩展变体：`md5(secret + msg)`、`sha1(secret + msg)` 这种前缀拼接最值得警惕。",
        "HMAC 使用错误：把 `hash(key || msg)` 当 HMAC、比较方式错误、截断不当，都可能出洞。",
        "Timing Attack：在线验证接口如果按字节比较签名，就可能被计时侧信道慢慢磨出来。",
        "碰撞变体：MD5、SHA1 出题通常不是要你正面找碰撞，而是利用现成碰撞性质或工具。",
        "CRC32 变体：它是线性校验，不是安全 MAC，题里单独出现时往往就是要你伪造。",
    ],
    "10_随机数预测": [
        "Python `random` 变体：题面源码直接用了 Mersenne Twister，就不要把它当密码学随机数。",
        "MT19937 状态恢复：给足够多输出时可以直接恢复内部 state，再预测后续 key/nonce。",
        "`random.seed(time)` 变体：只要 seed 落在可枚举时间窗里，密钥基本等于白给。",
        "短字符串 seed：seed 不是时间，而是几个字符、用户名、日期缩写时，也很适合爆破。",
        "LCG 变体：已知模数时恢复 `a,b`，未知模数时先从差分里恢复 `m`。",
        "语言实现变体：Java `Random`、C `rand`、numpy random、xorshift 的状态更新都不一样，要先认库。",
        "混合用法变体：随机数直接拿去做 AES key、CTR nonce、shuffle 顺序、验证码、token 时最容易出题。",
    ],
    "11_数学数论": [
        "CRT 变体：多模方程、广播攻击、Rabin、多组同余关系都可能落到中国剩余定理。",
        "离散对数变体：DLP、BSGS、Pohlig-Hellman、`p-1` 光滑这几种经常和 DH / ECC 混在一起。",
        "二次剩余变体：`x^2 ≡ a mod p`、Tonelli-Shanks、Legendre 符号题经常是某大题里的子步骤。",
        "连分数变体：不仅 Wiener 会用，很多“有理逼近”题也会把你往 continued fractions 上引。",
        "Pell 方程：虽然频率没 RSA 高，但题面一旦长成 `x^2 - D*y^2 = 1`，方向就很明确。",
        "高精度实数恢复：给你 `sqrt(2)`、`pi`、浮点近似值时，常见目标是恢复编码后的整数或文本。",
        "多项式环 / GF 变体：CRC、LFSR、NTRU、RLWE、有限域计算都可能以多项式模运算出现。",
    ],
    "12_协议类": [
        "Diffie-Hellman 变体：`p,g,A,B` 是最直接的外观信号，题点常在离散对数或参数校验。",
        "`p-1` 光滑：如果 DH 群阶很好分解，就别再把离散对数当成“理论上很难”。",
        "`g` 选得不好：`g=1`、`g=p-1`、小阶生成元都会让共享密钥空间极小。",
        "MITM 变体：协议没有认证时，中间人替换公钥往往比算数学更直接。",
        "SRP 弱参数：`A=0`、边界值没检查、共享密钥退化成固定值，是 CTF 很爱出的坑。",
        "JWT 变体：`alg=none`、`RS256 -> HS256`、弱 secret 爆破，虽然偏 Web，但本质还是 Crypto 错用。",
        "Cookie / 区块链变体：Flask/Django 签名伪造、交易签名重放、链上 ECDSA nonce 重用都归这里。",
    ],
    "13_签名算法": [
        "DSA / ECDSA nonce 重用：多份签名 `r` 相同几乎就是送分题，直接用公式恢复 `k` 和私钥。",
        "nonce 部分泄露：给高位、低位、偏差或多个近似 nonce 时，通常转成 HNP 或格攻击。",
        "`random.seed(...)` 生成 nonce：签名题一旦把随机源写弱，私钥就不再安全。",
        "Schnorr / EdDSA 变体：虽然公式不是 ECDSA 那套，但 nonce 出问题同样会炸私钥。",
        "RSA 签名伪造：低指数、小根、宽松 padding 验证、错误 hash 格式检查都是老考点。",
        "签名可塑性：某些算法里 `(r, n-s)` 仍然合法，看到“可改签名但消息不变”时要想到它。",
    ],
    "14_Padding": [
        "PKCS#7 变体：不仅要会补位，还要会识别“补位值等于补位长度”这个验证逻辑。",
        "CBC padding oracle：服务端只要能区分 padding 对错，就足以逐字节磨明文。",
        "CBC 相关变体：IV 可控、IV 固定、明文块对齐可操控时，经常和 padding / bit flipping 连在一起。",
        "PKCS#1 v1.5：RSA 加密和签名里都可能出题，经典方向是 Bleichenbacher 风格 oracle。",
        "OAEP 使用错误：随机数固定、验证顺序不对、实现细节漏错时也可能成为突破口。",
        "Padding 类题别只看对称密码，RSA padding oracle 同样是高频老朋友。",
    ],
    "15_图片音频文件混合Crypto": [
        "图片变体：黑白像素、RGB 奇偶、二维码、两种字体/颜色差异，经常先转成 bit 再进 Crypto。",
        "音频变体：滴滴声摩斯、频谱图藏字、采样值奇偶取 bit，都属于高频混合题。",
        "文档变体：Word / PDF 里的白色文字、批注、隐藏对象、字体差异经常只是第一层载体。",
        "文件头变体：提取出来的东西可能不是文本，而是压缩包、图片、PE 文件，再往下还有一层。",
        "组合变体：图片 + Bacon + Base64、图片 XOR、二维码 -> Base64 -> AES/RSA 这些链路非常常见。",
    ],
    "16_自定义密码": [
        "可逆运算变体：加减、异或、移位、循环位移、取模截断，只要步骤清楚通常都能逆。",
        "置换变体：`c[i] = m[perm[i]]`、索引交换、块内重排，本质都是先求逆置换。",
        "shuffle 变体：如果用了 `random.shuffle`，关键不在打乱本身，而在 seed 能不能恢复。",
        "矩阵加密：矩阵乘法、模运算、Hill 风格都要先问自己“能不能求逆矩阵”。",
        "GF(2) 方程组：大量 xor 约束时，别死算，直接转高斯消元或位线性系统。",
        "Z3 / SMT 变体：分支多、约束硬、人工逆不顺时，建模给求解器反而更快。",
        "自定义分组密码：魔改 Feistel、TEA 套壳、白盒逻辑都要先把每轮状态更新写清楚。",
    ],
    "17_脑洞类Crypto": [
        "题名伪装：`baby_rsa`、`ezAES`、`Rabbit`、`Affine` 这类标题常常直接把算法名字塞给你。",
        "文件名 / 附件名提示：`bacon.png`、`cipher.txt`、`key.pem`、`random.py` 往往比题面正文更诚实。",
        "结构提示伪装：看起来像随机串，但如果明文前后缀、flag 格式可预测，就要反过来利用结构。",
        "假 Crypto 真编码：不少题表面挂着 Crypto，其实只是编码套娃、古典密码或首字母藏信息。",
        "混合题提示：当附件是图片、音频、脚本源码时，往往不是让你只看一种题型，而是让你先分类。",
    ],
    "18_组合套娃": [
        "RSA + AES：RSA 不直接解 flag，而是先解出对称密钥、IV 或私钥文件密码。",
        "随机数 + AES：seed 爆掉以后，AES key / nonce 也就跟着出来了。",
        "LFSR + XOR：先恢复 keystream，再把密文异或回去，是非常常见的双层题。",
        "图片 + Bacon + Base64：先提取视觉层，再做古典映射，最后才落到普通解码。",
        "区块链 + ECDSA：交易数据、`r/s/v`、签名恢复、公钥恢复经常连成一整套。",
        "PEM + RSA + OpenSSL：证书、公钥、私钥、文件封装格式本身也可能是题目的一层壳。",
    ],
}


def build_variant_section(folder: str, bullets: list[str]) -> str:
    lines = [
        SECTION_TITLE,
        "",
        "下面这些高频变体来自 `C:\\Users\\yu\\Downloads\\1.txt`，实战里如果题面长得像这些伪装方式，也可以直接往这一类靠：",
        "",
    ]
    lines.extend(f"- {bullet}" for bullet in bullets)
    lines.append("")
    return "\n".join(lines)


def update_readme(path: Path, bullets: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace(SOURCE_INTRO_OLD, SOURCE_INTRO_NEW)
    new_section = build_variant_section(path.parent.name, bullets)

    if SECTION_TITLE in text:
        before, rest = text.split(SECTION_TITLE, 1)
        _, after = rest.split(INSERT_BEFORE, 1)
        text = before.rstrip() + "\n\n" + new_section + "\n" + INSERT_BEFORE + after
    else:
        before, after = text.split(INSERT_BEFORE, 1)
        text = before.rstrip() + "\n\n" + new_section + "\n" + INSERT_BEFORE + after

    path.write_text(text, encoding="utf-8")


def update_index(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "整理来源：`C:\\Users\\yu\\Downloads\\2.txt`",
        "整理来源：`C:\\Users\\yu\\Downloads\\2.txt`、`C:\\Users\\yu\\Downloads\\1.txt`",
    )
    text = text.replace(
        "- `README.md`：讲清楚这类题的表述、背景、识别信号、什么时候该想到它。",
        "- `README.md`：讲清楚这类题的表述、背景、识别信号、什么时候该想到它，以及高频变体和常见伪装方式。",
    )
    marker = "这个目录按“大题型”拆分，每个题型文件夹里都有两份内容："
    note = marker + "\n\n本次已经把 `1.txt` 里的变体题型并入各目录的 `README.md`。"
    if marker in text and "本次已经把 `1.txt` 里的变体题型并入各目录的 `README.md`。" not in text:
        text = text.replace(marker, note)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for root in ROOTS:
        if not root.exists():
            continue
        index_path = root / "00_总索引.md"
        if index_path.exists():
            update_index(index_path)
        for folder, bullets in VARIANTS.items():
            readme_path = root / folder / "README.md"
            if readme_path.exists():
                update_readme(readme_path, bullets)
        print(f"updated variants under {root}")


if __name__ == "__main__":
    main()

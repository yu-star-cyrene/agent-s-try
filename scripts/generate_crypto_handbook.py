from __future__ import annotations

from pathlib import Path
from textwrap import dedent


OUTPUT_DIR = Path("tmp_crypto_handbook")
SOURCE_FILE = r"C:\Users\yu\Downloads\2.txt"


TOPICS = [
    {
        "folder": "01_古典密码",
        "title": "古典密码",
        "summary": "以字母替换、位置重排、查表映射为主的入门型 Crypto 题。",
        "background": "这类题大多来自传统手工密码，重点不是现代密码学强度，而是看你能不能从字母分布、排布方式、题目提示词里迅速认出套路。",
        "when_to_think": [
            "密文主要由英文字母组成，而且看起来像被整体平移、周期偏移或重排过。",
            "题目名或描述里出现 `caesar`、`shift`、`rot13`、`vigenere`、`fence`、`bacon`、`morse`、`pigpen`、`braille` 之类关键词。",
            "出现大小写混合、点横、A/B、0/1、W 型排列、矩阵按列读等非常有“规则感”的模式。",
            "附件是图片、文本、符号表，但数据量不大，更像是查表或爆破小参数。",
        ],
        "data_signals": [
            "全字母串，长度不长，像英文但读不通。",
            "提示里强调 `key`、`keyword`、`row/column`、`rail fence`、`affine`。",
            "密文由两种符号组成，且每 5 位、每 8 位、每组点横有明显分隔。",
            "小人图案、猪圈图案、盲文点阵、键盘位移、T9 数字映射等非标准字母表示。",
        ],
        "subtypes": [
            "凯撒、ROT13、仿射、维吉尼亚",
            "栅栏密码、列置换密码",
            "培根密码、摩斯密码",
            "猪圈、跳舞小人、盲文、键盘密码、T9、云影/当铺/曲路密码",
        ],
        "starter_steps": [
            "先判断是“替换”还是“重排”。替换类优先爆破偏移、查表、频率；重排类优先枚举行列或还原矩阵。",
            "如果只有两种字符，优先想到 Bacon、Morse、二进制、Braille 的编码映射。",
            "如果题目给了 key 或 keyword，优先尝试 Vigenere、列置换或键盘位移。",
            "先不用急着写复杂代码，很多古典密码先靠识别题型就已经赢一半。",
        ],
        "pitfalls": [
            "不要只盯着凯撒，很多“看起来像乱英文”的题其实是 Vigenere、Rail Fence 或 Columnar。",
            "Morse、Bacon、Braille 经常有反转、倒序、大小写映射互换等变种。",
            "图片里出现两种颜色、两种字体时，不一定是隐写，也可能只是古典密码载体。",
        ],
        "script_focus": "脚本演示凯撒爆破、ROT13 和已知 key 的维吉尼亚解密，适合作为古典密码第一手模板。",
        "example_code": dedent(
            """
            from string import ascii_lowercase


            def caesar_bruteforce(text: str) -> None:
                for shift in range(26):
                    out = []
                    for ch in text:
                        if ch.isalpha():
                            base = ord("A") if ch.isupper() else ord("a")
                            out.append(chr((ord(ch) - base - shift) % 26 + base))
                        else:
                            out.append(ch)
                    print(f"shift={shift:02d}: {''.join(out)}")


            def rot13(text: str) -> str:
                return text.translate(
                    str.maketrans(
                        ascii_lowercase + ascii_lowercase.upper(),
                        ascii_lowercase[13:] + ascii_lowercase[:13] +
                        (ascii_lowercase[13:] + ascii_lowercase[:13]).upper(),
                    )
                )


            def vigenere_decrypt(ciphertext: str, key: str) -> str:
                key = key.lower()
                out = []
                idx = 0
                for ch in ciphertext:
                    if ch.isalpha():
                        base = ord("A") if ch.isupper() else ord("a")
                        shift = ord(key[idx % len(key)]) - ord("a")
                        out.append(chr((ord(ch) - base - shift) % 26 + base))
                        idx += 1
                    else:
                        out.append(ch)
                return "".join(out)


            if __name__ == "__main__":
                cipher = "khoor"
                caesar_bruteforce(cipher)
                print("ROT13:", rot13("synt"))
                print("Vigenere:", vigenere_decrypt("rijvs", "key"))
            """
        ).strip()
        + "\n",
    },
    {
        "folder": "02_编码与变换",
        "title": "编码与变换",
        "summary": "更像是数据表示层的变换，不一定是真正的加密，但在 CTF 里经常作为第一层壳。",
        "background": "这类题的核心是认字符集、认分隔符、认数据长度。很多时候题目并不难，难在你有没有第一时间想到去做 decode。",
        "when_to_think": [
            "密文看起来像规范编码串，比如以 `=` 结尾、只含十六进制字符、只含 `0/1` 或 `%xx`。",
            "题目提示 `base`、`hex`、`ascii`、`unicode`、`url`、`html entity`、`endian`、`binary`。",
            "数据层层包裹，解开一层后还是另一种编码。",
            "密文不是随机字节，而是明显可打印字符的规则组合。",
        ],
        "data_signals": [
            "`=` 结尾，多半先查 Base64/Base32。",
            "只含 `0-9a-fA-F` 且长度为偶数，多半先试 Hex。",
            "只含大写字母和 `2-7`，多半是 Base32。",
            "出现 `%66%6c%61%67`、`&#102;`、`\\u0066` 这类转义串，优先做 URL/HTML/Unicode 解码。",
            "长串 01 先按 8 位、7 位、5 位分组，再考虑二进制、Bacon、Morse。",
        ],
        "subtypes": [
            "Base64、Base32、Base16/Hex、Base58、Base85/Ascii85",
            "URL 编码、Unicode 编码、HTML 实体编码",
            "ASCII 数字、二进制、八进制、十六进制反转、大小端转换",
            "多层套娃编码",
        ],
        "starter_steps": [
            "先看字符集和尾巴，再看长度是否像某种编码的合法输出。",
            "从最便宜的解码开始：Hex、Base64、Base32、URL、ASCII、Binary。",
            "每解一层都要重新观察结果，不要默认只有一层。",
            "如果解出来像乱码，检查大小端、反转、去空格、去换行、补齐 padding。",
        ],
        "pitfalls": [
            "Base64 和 Base32 很容易因为缺少 padding 导致误判，记得手动补 `=`。",
            "纯十六进制不一定直接是明文，也可能是 XOR/AES/RSA 的密文表示。",
            "01 串别只按 8 位切，很多题会故意让你按 5 位、7 位或者倒序。",
        ],
        "script_focus": "脚本按常见顺序尝试 Hex、Base64、Base32、URL，并展示一个简单的多层解码思路。",
        "example_code": dedent(
            """
            import base64
            import binascii
            from urllib.parse import unquote


            def try_hex(text: str):
                try:
                    return bytes.fromhex(text).decode()
                except Exception:
                    return None


            def try_b64(text: str):
                padding = "=" * (-len(text) % 4)
                try:
                    return base64.b64decode(text + padding).decode()
                except Exception:
                    return None


            def try_b32(text: str):
                padding = "=" * (-len(text) % 8)
                try:
                    return base64.b32decode(text + padding).decode()
                except Exception:
                    return None


            def layered_decode(text: str) -> None:
                current = text.strip()
                for name, fn in [("hex", try_hex), ("base64", try_b64), ("base32", try_b32)]:
                    value = fn(current)
                    if value is not None:
                        print(f"[{name}] {value}")
                print("[url ]", unquote(current))


            if __name__ == "__main__":
                layered_decode("666c6167")
                layered_decode("ZmxhZw==")
                layered_decode("%66%6c%61%67")
            """
        ).strip()
        + "\n",
    },
    {
        "folder": "03_XOR异或",
        "title": "XOR 异或",
        "summary": "CTF 里最高频的基础套路之一，既能单独出题，也常被放进多层套娃里。",
        "background": "异或本质上是可逆线性运算，`c = m ^ k` 的最大弱点通常不是公式本身，而是密钥太短、可重复、可猜、或出现已知明文。",
        "when_to_think": [
            "题目明说 `xor`、`key`、`one-time pad`、`stream`、`two-time pad`。",
            "密文是 hex/base64 包裹的随机字节，但长度和文本长度接近。",
            "有两份或多份密文看起来使用了同一密钥。",
            "flag 格式已知，或明文前缀高度可猜，例如 `flag{`、PNG 头、`PK`。",
        ],
        "data_signals": [
            "单字节 XOR 常见于短密文、给你一段 hex，解出来应是可打印文本。",
            "循环 XOR 常见于 key 比较短，密文很长，可以按列分组分析。",
            "两份密文同 key 时，`c1 ^ c2 = m1 ^ m2`，已知一份明文就能推出另一份。",
            "图片 XOR 时，经常有固定文件头可做已知明文攻击。",
        ],
        "subtypes": [
            "单字节 XOR",
            "多字节循环 XOR",
            "双密文共用密钥 / two-time pad",
            "图片 XOR",
            "XOR 与 Base64/Hex 套娃",
        ],
        "starter_steps": [
            "先判断密文是原始字节、hex 还是 base64 表示。",
            "如果是单字节 XOR，直接枚举 0~255，按可打印性或 flag 格式筛答案。",
            "如果是循环 XOR，优先利用已知 flag 头、猜 key 长度、按列做单字节分析。",
            "如果有多份密文，先互相异或，找能利用的结构信息。",
        ],
        "pitfalls": [
            "循环 XOR 不一定是英文字母 key，也可能是任意字节。",
            "不要只看明文是否都是 ASCII，有些题解出来可能是压缩包、图片或下一层编码。",
            "密文长度如果非常整齐，也可能是块密码输出而不是 XOR。",
        ],
        "script_focus": "脚本包含单字节 XOR 爆破和循环 XOR 解密模板，是最常见的实战骨架。",
        "example_code": dedent(
            """
            from string import printable


            def score_text(data: bytes) -> int:
                return sum(chr(b) in printable for b in data)


            def brute_single_byte_xor(cipher: bytes) -> None:
                best = []
                for key in range(256):
                    plain = bytes(b ^ key for b in cipher)
                    best.append((score_text(plain), key, plain))
                for _, key, plain in sorted(best, reverse=True)[:10]:
                    print(f"key={key:02x} -> {plain}")


            def repeating_key_xor(cipher: bytes, key: bytes) -> bytes:
                return bytes(cipher[i] ^ key[i % len(key)] for i in range(len(cipher)))


            if __name__ == "__main__":
                brute_single_byte_xor(bytes.fromhex("2326292c"))
                cipher = bytes.fromhex("0d09180c0e")
                print(repeating_key_xor(cipher, b"key"))
            """
        ).strip()
        + "\n",
    },
    {
        "folder": "04_流密码",
        "title": "流密码",
        "summary": "把密钥流逐字节与明文异或的加密方式，题目常从 keystream、LFSR、RC4、ChaCha 或弱随机源下手。",
        "background": "流密码的常见破绽不是“异或本身”，而是密钥流生成器弱、nonce 重用、状态可恢复、随机数种子可预测。",
        "when_to_think": [
            "题目给你连续输出流、比特流、寄存器状态或 `x ^= x << a` 这类状态更新式。",
            "关键词出现 `RC4`、`ChaCha20`、`Salsa20`、`Rabbit`、`LFSR`、`MT19937`。",
            "给了很多伪随机输出，希望你恢复 seed 或 state。",
            "同一个 keystream/nonce 被重复使用，导致多个密文之间存在线性关系。",
        ],
        "data_signals": [
            "长串 `0/1`、寄存器抽头、反馈多项式，优先想到 LFSR。",
            "给你 624 个 Python random 输出，优先想到 MT19937 状态恢复。",
            "给出 `nonce`、`counter`、`state`、`keystream` 等字段，多半是流密码或 PRNG 题。",
            "如果密文只是明文与字节流异或，且 key/nonce 来自弱随机数，就要联想到 seed 爆破。",
        ],
        "subtypes": [
            "RC4、Rabbit、Salsa20、ChaCha20",
            "LFSR 及多个 LFSR 组合",
            "MT19937、xorshift、弱随机流",
        ],
        "starter_steps": [
            "先搞清楚这是“标准流密码”还是“自制 keystream XOR”。",
            "如果看到位级反馈或移位，先把状态更新函数抄清楚，再考虑逆推。",
            "如果看到时间戳、`random.seed(time)`、`nonce` 重用，先走最便宜的爆破和复用攻击。",
            "能拿到已知明文时，优先恢复 keystream 再解剩余部分。",
        ],
        "pitfalls": [
            "不要把所有异或题都归到普通 XOR，题目可能真正想考的是 keystream 生成器。",
            "LFSR 题经常需要按位而不是按字节理解。",
            "标准算法题里最常见的坑是 nonce/key 重用，而不是算法被暴力破解。",
        ],
        "script_focus": "脚本演示一个玩具 LFSR 生成 keystream 并做 XOR 解密，方便你在同类题里先搭出状态机。",
        "example_code": dedent(
            """
            def lfsr_step(state: int, taps: tuple[int, ...], width: int) -> tuple[int, int]:
                feedback = 0
                for tap in taps:
                    feedback ^= (state >> tap) & 1
                out = state & 1
                state = (state >> 1) | (feedback << (width - 1))
                return state, out


            def keystream(seed: int, taps: tuple[int, ...], width: int, nbits: int) -> list[int]:
                state = seed
                out = []
                for _ in range(nbits):
                    state, bit = lfsr_step(state, taps, width)
                    out.append(bit)
                return out


            def bits_to_bytes(bits: list[int]) -> bytes:
                out = bytearray()
                for i in range(0, len(bits), 8):
                    chunk = bits[i:i + 8]
                    value = 0
                    for bit in chunk:
                        value = (value << 1) | bit
                    out.append(value)
                return bytes(out)


            if __name__ == "__main__":
                cipher = bytes.fromhex("031d0b")
                bits = keystream(seed=0b10101, taps=(0, 2), width=5, nbits=len(cipher) * 8)
                key = bits_to_bytes(bits)
                plain = bytes(c ^ k for c, k in zip(cipher, key))
                print("keystream =", key.hex())
                print("plaintext =", plain)
            """
        ).strip()
        + "\n",
    },
    {
        "folder": "05_分组密码",
        "title": "分组密码",
        "summary": "以 AES、DES、TEA、Feistel 为主，识别重点通常在模式、IV、padding、oracle 和重复块。",
        "background": "分组密码题很少要求你暴力破解 AES 本身，真正能做题的地方往往是模式用错了、参数复用了、服务端返回了侧信道信息。",
        "when_to_think": [
            "题目给出 `key`、`iv`、`nonce`、`ciphertext`、`tag`、`mode`。",
            "密文长度总是 16 的倍数，或者能明显分成固定大小块。",
            "题目关键词包含 `ECB`、`CBC`、`CTR`、`GCM`、`DES`、`TEA`、`Feistel`。",
            "服务端会告诉你 padding 错误、认证失败或允许你改密文再提交。",
        ],
        "data_signals": [
            "重复明文块对应重复密文块，多半是 ECB。",
            "给了 `iv` 并且密文按块组织，多半是 CBC/CTR 一类。",
            "给 `nonce` 和 `tag`，优先想到 CTR/GCM/ChaCha 生态。",
            "`delta = 0x9e3779b9` 很像 TEA/XTEA 家族。",
        ],
        "subtypes": [
            "AES-ECB、AES-CBC、AES-CTR、AES-GCM",
            "CBC bit flipping、CBC padding oracle",
            "DES 弱密钥",
            "TEA / XTEA / XXTEA、自定义 Feistel",
        ],
        "starter_steps": [
            "先按 16 字节切块，观察是否有重复块、固定 IV、奇怪的块边界。",
            "如果题目能交互，先试修改某个块，看看服务端是 padding 错误还是内容错误。",
            "如果题目只给参数，优先复现一遍本地解密流程，确认模式和编码没有看错。",
            "对于自定义 Feistel/TEA，先把轮函数和轮数抄成代码，再做逆过程。",
        ],
        "pitfalls": [
            "很多题解不出来不是算法难，而是 key、iv、ciphertext 的编码没处理对。",
            "CBC 位翻转只能精确控制下一块明文，不要改错目标块。",
            "GCM 如果 nonce 重用会非常危险，但前提是你要确认确实用了同 key 同 nonce。",
        ],
        "script_focus": "脚本演示 AES-ECB/CBC 的本地解密模板，以及一个快速检测 ECB 重复块的小函数。",
        "example_code": dedent(
            """
            try:
                from Crypto.Cipher import AES
                from Crypto.Util.Padding import unpad
            except ImportError:
                raise SystemExit("请先安装 pycryptodome: pip install pycryptodome")


            def detect_ecb(ciphertext: bytes, block_size: int = 16) -> bool:
                blocks = [ciphertext[i:i + block_size] for i in range(0, len(ciphertext), block_size)]
                return len(blocks) != len(set(blocks))


            def aes_ecb_decrypt(key: bytes, ciphertext: bytes) -> bytes:
                cipher = AES.new(key, AES.MODE_ECB)
                return unpad(cipher.decrypt(ciphertext), 16)


            def aes_cbc_decrypt(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
                cipher = AES.new(key, AES.MODE_CBC, iv=iv)
                return unpad(cipher.decrypt(ciphertext), 16)


            if __name__ == "__main__":
                demo = b"A" * 32
                print("ECB repeated blocks:", detect_ecb(demo))
            """
        ).strip()
        + "\n",
    },
    {
        "folder": "06_RSA",
        "title": "RSA",
        "summary": "CTF Crypto 的核心重灾区，真正考点几乎都来自参数弱点和额外泄露。",
        "background": "RSA 题不是背公式，而是找破绽。只要你先判断出题目给的是哪种泄露，后面就是分解、求逆、开根、CRT、Coppersmith 这几类武器的组合。",
        "when_to_think": [
            "附件或数据里出现 `n`、`e`、`c`、`p`、`q`、`phi`、`dp`、`dq`、`d`。",
            "看到 `.pem`、`.pub`、证书、公钥文件、十进制大整数文本。",
            "多个模数 `n1, n2, ...` 同时出现，或者 `e=3/5/17/65537` 被特别强调。",
            "密文是大整数，且所有关键参数都围绕模幂运算展开。",
        ],
        "data_signals": [
            "`n, e, c` 是最典型的识别信号。",
            "`dp`、`dq`、`d`、`phi`、`p+q`、`p-q`、`p xor q`、高低位泄露都在暗示特定攻击。",
            "`多个 n`、`相同 e`、`相同明文`、`相关明文` 对应共因子、广播、共模、Franklin-Reiter。",
            "`e=2/3`、`d 很小`、`p≈q`、`n 可分解` 都是经典弱点。",
        ],
        "subtypes": [
            "基础解密、直接分解、Fermat 分解",
            "Common Modulus、低指数、广播攻击",
            "dp/dq/d/phi 泄露、高低位泄露",
            "Wiener、Boneh-Durfee、Coppersmith、相关明文、oracle 类",
        ],
        "starter_steps": [
            "先列清题目到底给了哪些参数，再对照常见攻击分类。",
            "先做最便宜的事：分解 `n`、多模数两两 gcd、检查 `e` 是否很小、检查 `p≈q`。",
            "如果有额外泄露，优先看是 CRT 类恢复、连分数类攻击，还是小根问题。",
            "如果有交互服务，再考虑 parity oracle、padding oracle、签名伪造。",
        ],
        "pitfalls": [
            "不要一上来就找高端攻击，很多 RSA 题先做 gcd、直接分解就够了。",
            "`c` 很小并不总是能直接开根，还要确认 `m^e < n` 或满足广播条件。",
            "当题目给的是十六进制/字节串时，先别忘了把编码转成整数。",
        ],
        "script_focus": "脚本提供最常用的 RSA 解密骨架，并顺手给出多模数 gcd 排查模板。",
        "example_code": dedent(
            """
            from math import gcd


            def egcd(a: int, b: int) -> tuple[int, int, int]:
                if b == 0:
                    return a, 1, 0
                g, x1, y1 = egcd(b, a % b)
                return g, y1, x1 - (a // b) * y1


            def inverse(a: int, m: int) -> int:
                g, x, _ = egcd(a, m)
                if g != 1:
                    raise ValueError("inverse does not exist")
                return x % m


            def long_to_bytes(value: int) -> bytes:
                size = max(1, (value.bit_length() + 7) // 8)
                return value.to_bytes(size, "big")


            def rsa_decrypt(n: int, e: int, c: int, p: int, q: int) -> bytes:
                phi = (p - 1) * (q - 1)
                d = inverse(e, phi)
                m = pow(c, d, n)
                return long_to_bytes(m)


            def scan_common_factor(moduli: list[int]) -> None:
                for i in range(len(moduli)):
                    for j in range(i + 1, len(moduli)):
                        g = gcd(moduli[i], moduli[j])
                        if g != 1:
                            print(f"n[{i}] and n[{j}] share factor {g}")


            if __name__ == "__main__":
                print("把 n/e/c/p/q 替换成题目参数后直接跑。")
            """
        ).strip()
        + "\n",
    },
    {
        "folder": "07_ECC椭圆曲线",
        "title": "ECC 椭圆曲线",
        "summary": "围绕椭圆曲线群运算、离散对数、ECDH/ECDSA 的题型，核心是识别曲线参数和群结构是否有弱点。",
        "background": "ECC 题一旦能认出 `a, b, p, G, Q` 这一套参数，就说明方向已经对了。真正突破点通常是小阶子群、光滑阶、异常/奇异曲线、私钥太小，或者 nonce 使用失误。",
        "when_to_think": [
            "题目给出曲线方程参数 `a, b, p`，以及点 `G, Q, P`。",
            "出现 `ECDH`、`ECDSA`、`nonce`、`r/s`、`curve`、`point`、`scalar multiplication`。",
            "数据不是普通整数，而是点坐标对 `(x, y)`。",
            "题目提示曲线阶、子群阶、MOV、anomalous、singular 等术语。",
        ],
        "data_signals": [
            "`a, b, p, G` 几乎就是 ECC 身份证。",
            "两次签名 `r` 相同，多半是 ECDSA nonce 重用。",
            "阶很光滑、点阶很小，说明可以考虑 Pohlig-Hellman 或小阶子群攻击。",
            "如果题目特别强调曲线异常、奇异或 embedding degree，说明要跳出普通 DLP 思路。",
        ],
        "subtypes": [
            "基础点加、倍点、标量乘",
            "ECDH 共享密钥恢复",
            "小阶子群、Pohlig-Hellman、MOV、异常曲线、奇异曲线",
            "ECDSA/EdDSA nonce 重用或部分泄露",
        ],
        "starter_steps": [
            "先确认点是否在曲线上，再写出点加和标量乘模板。",
            "如果目标是离散对数，先看群阶是否小、是否光滑、是否存在弱子群。",
            "如果是签名题，优先排查 nonce 是否重用、过小或部分泄露。",
            "如果是 ECDH，先看有没有办法求出某一方私钥或把点送进弱子群。",
        ],
        "pitfalls": [
            "ECC 题很怕抄错模数和坐标，代码里每一步都要保持 mod p。",
            "不要默认所有点都在大素数阶群里，很多 CTF 就靠坏曲线或坏子群出题。",
            "签名题里 `r` 相同极其敏感，看到就要立刻想到 nonce 重用。",
        ],
        "script_focus": "脚本实现玩具曲线的点加和标量乘，便于你先把题目给的曲线参数代进去验证方向。",
        "example_code": dedent(
            """
            O = None


            def inverse(a: int, p: int) -> int:
                return pow(a, -1, p)


            def point_add(P, Q, a: int, p: int):
                if P is O:
                    return Q
                if Q is O:
                    return P
                x1, y1 = P
                x2, y2 = Q
                if x1 == x2 and (y1 + y2) % p == 0:
                    return O
                if P != Q:
                    lam = ((y2 - y1) * inverse(x2 - x1, p)) % p
                else:
                    lam = ((3 * x1 * x1 + a) * inverse(2 * y1, p)) % p
                x3 = (lam * lam - x1 - x2) % p
                y3 = (lam * (x1 - x3) - y1) % p
                return x3, y3


            def scalar_mul(k: int, P, a: int, p: int):
                result = O
                addend = P
                while k:
                    if k & 1:
                        result = point_add(result, addend, a, p)
                    addend = point_add(addend, addend, a, p)
                    k >>= 1
                return result


            if __name__ == "__main__":
                a, b, p = 2, 3, 97
                G = (3, 6)
                print("2G =", scalar_mul(2, G, a, p))
                print("5G =", scalar_mul(5, G, a, p))
            """
        ).strip()
        + "\n",
    },
    {
        "folder": "08_格密码与LLL",
        "title": "格密码与 LLL",
        "summary": "题目经常伪装成背包、小根、部分泄露、近似方程，本质上是在考格构造和约化。",
        "background": "这类题比前几类更数学，但识别信号其实很鲜明：高位/低位泄露、小根、短向量、近似关系、subset sum、Hidden Number Problem 都是典型入口。",
        "when_to_think": [
            "题目出现 `LLL`、`lattice`、`small root`、`subset sum`、`knapsack`、`NTRU`、`LWE`。",
            "给了高位/低位泄露、部分比特、近似方程，希望你恢复完整秘密。",
            "很多未知量满足线性关系，但又不是精确方程，更像“近似成立”。",
            "RSA/ECDSA 题里出现部分私钥、部分 nonce 时，也可能转成格问题。",
        ],
        "data_signals": [
            "背包权重和目标和，对应 subset sum / knapsack。",
            "形如 `x 很小`、`f(x) mod n = 0` 的描述，常是 Coppersmith 小根。",
            "部分 nonce、高位泄露、低位泄露，常见于 HNP 或小根。",
            "题目要求找“短向量”“最近向量”“满足约束的整数解”，优先考虑 SVP/CVP/LLL。",
        ],
        "subtypes": [
            "背包密码、子集和",
            "Coppersmith 小根",
            "Hidden Number Problem",
            "NTRU、LWE / RLWE、CVP / SVP",
        ],
        "starter_steps": [
            "先别急着上 LLL，先判断是不是小规模题，可以直接爆破或 meet-in-the-middle。",
            "如果是部分泄露，先把已知部分和未知部分写成多项式或线性关系。",
            "如果是背包题，先确认是超递增还是一般 subset sum。",
            "真正需要格时，再考虑如何构造基向量和权重缩放。",
        ],
        "pitfalls": [
            "不是所有“有很多未知数”的题都该上 LLL，很多时候先写出精确方程更重要。",
            "格构造最怕尺度不对，量纲差太大时 LLL 结果会很难看。",
            "这类题经常需要 Sage/fpylll，但你至少要先想清楚目标变量是什么。",
        ],
        "script_focus": "脚本用一个小型 subset sum 演示“看到背包就先把目标和和权重列出来”的基本思路。",
        "example_code": dedent(
            """
            from itertools import combinations


            def subset_sum(weights: list[int], target: int):
                for r in range(1, len(weights) + 1):
                    for picks in combinations(range(len(weights)), r):
                        total = sum(weights[i] for i in picks)
                        if total == target:
                            return picks
                return None


            if __name__ == "__main__":
                weights = [2, 5, 9, 13, 21]
                target = 34
                answer = subset_sum(weights, target)
                print("picked indices =", answer)
                if answer is not None:
                    print("picked values  =", [weights[i] for i in answer])
            """
        ).strip()
        + "\n",
    },
    {
        "folder": "09_哈希与MAC",
        "title": "哈希与 MAC",
        "summary": "重点不是“反推出原文”，而是识别哈希用途、是否可爆破、是否存在长度扩展或错误的签名/比较方式。",
        "background": "哈希题常常混在 Web、登录验证、文件校验和 Crypto 之间。真正有用的切入点通常是弱口令、长度扩展、碰撞、CRC32 可伪造、HMAC 使用错误、计时侧信道。",
        "when_to_think": [
            "看到 32/40/64 位十六进制摘要，或者 `md5`、`sha1`、`sha256`、`hmac`、`mac`、`crc32`。",
            "题目要求伪造签名、绕过校验、恢复短明文或比较哈希值。",
            "服务端使用 `md5(secret + msg)` 这类前缀 MAC。",
            "同一摘要对应不同文件、或者题目刻意提到碰撞、长度扩展、timing。",
        ],
        "data_signals": [
            "32 hex 常见 MD5，40 hex 常见 SHA1，64 hex 常见 SHA256。",
            "`md5(secret+msg)`、`sha1(secret+msg)` 常见长度扩展入口。",
            "`crc32` 不是安全 MAC，很多题会让你伪造校验值。",
            "签名比较如果逐字节返回失败位置，可能有 Timing Attack。",
        ],
        "subtypes": [
            "哈希爆破、彩虹表/在线查询",
            "长度扩展攻击",
            "MD5/SHA1 碰撞",
            "CRC32 伪造、HMAC 错误使用、Timing Attack",
        ],
        "starter_steps": [
            "先识别摘要类型和输出长度，判断是爆破题还是协议/伪造题。",
            "如果明文短、规则强，优先字典爆破或掩码爆破。",
            "如果是 MAC，先确认是 HMAC 还是自己拼接的 `hash(secret || msg)`。",
            "如果是在线服务，观察返回时间和错误信息是否泄露比较过程。",
        ],
        "pitfalls": [
            "标准 HMAC 不吃长度扩展，别把前缀哈希和 HMAC 混了。",
            "看到 MD5 也别默认一定是碰撞题，很多时候就是普通口令爆破。",
            "CRC32 是线性的，不是安全摘要；题目里单独出现它往往就是突破口。",
        ],
        "script_focus": "脚本先按常见摘要长度识别算法，再做一个小字典爆破示例，适合最常见的 hash 入门题。",
        "example_code": dedent(
            """
            import hashlib


            def guess_hash_type(digest: str) -> str:
                mapping = {32: "md5", 40: "sha1", 64: "sha256"}
                return mapping.get(len(digest), "unknown")


            def brute_wordlist(digest: str, words: list[str]) -> None:
                kind = guess_hash_type(digest)
                if kind == "unknown":
                    print("未知摘要长度，先别盲爆。")
                    return
                for word in words:
                    h = getattr(hashlib, kind)(word.encode()).hexdigest()
                    if h == digest.lower():
                        print(f"match: {word} ({kind})")
                        return
                print("wordlist miss")


            if __name__ == "__main__":
                target = hashlib.md5(b"flag").hexdigest()
                brute_wordlist(target, ["hello", "test", "flag", "admin"])
            """
        ).strip()
        + "\n",
    },
    {
        "folder": "10_随机数预测",
        "title": "随机数预测",
        "summary": "题目本质不是密码学本身，而是生成密钥、nonce、shuffle 顺序的随机源太弱。",
        "background": "在 CTF 里，`random`、`seed(time)`、LCG、xorshift 这类可预测随机数非常常见。只要能恢复 seed 或 state，后面的 key、IV、nonce 往往就跟着出来了。",
        "when_to_think": [
            "看到 `random`、`seed`、时间戳、`rand()`、LCG 参数、伪随机输出序列。",
            "题目源码里用 Python `random`、C `rand`、Java `Random`、numpy random 生成 key/nonce。",
            "服务端返回连续随机数，要求你预测下一次输出。",
            "随机数又被拿去做加密 key、打乱顺序、验证码或 token。",
        ],
        "data_signals": [
            "`seed = time`、`int(time.time())` 是最经典的爆破点。",
            "给出多个输出和公式 `x_{n+1} = a*x_n + b mod m`，优先想到 LCG。",
            "给出 624 个 Python random 输出，优先想到 MT19937。",
            "如果随机流直接当作 XOR keystream，用已知明文恢复 seed 更香。",
        ],
        "subtypes": [
            "Python random、`random.seed(time)`",
            "numpy random、Java Random、C rand",
            "LCG、Blum Blum Shub、xorshift",
            "弱随机流加密",
        ],
        "starter_steps": [
            "先确认随机数来自哪套实现，再判断是爆 seed 还是恢复内部状态。",
            "如果 seed 跟时间有关，先缩小时间窗口，做区间爆破。",
            "如果输出很多，优先想状态恢复，而不是硬猜 key。",
            "如果随机数参与了 shuffle 或生成 bytes，先把转换过程复现出来。",
        ],
        "pitfalls": [
            "Python `random` 不是密码安全随机数，但 Python `secrets`/`os.urandom` 不是一个级别。",
            "时间戳爆破时要注意时区、毫秒/秒、取整方式。",
            "看到随机数别只想单次输出，很多题真正可利用的是“连续观测”。",
        ],
        "script_focus": "脚本模拟 `random.seed(time)` 生成密钥，并在时间窗口内爆破 seed 恢复明文，是非常典型的比赛套路。",
        "example_code": dedent(
            """
            import random
            import time


            def encrypt_with_time_seed(plaintext: bytes, seed: int) -> bytes:
                rng = random.Random(seed)
                key = bytes(rng.randrange(256) for _ in range(len(plaintext)))
                return bytes(p ^ k for p, k in zip(plaintext, key))


            def brute_seed(ciphertext: bytes, known_prefix: bytes, start: int, end: int):
                for seed in range(start, end + 1):
                    plain = encrypt_with_time_seed(ciphertext, seed)
                    if plain.startswith(known_prefix):
                        return seed, plain
                return None, None


            if __name__ == "__main__":
                seed = int(time.time())
                cipher = encrypt_with_time_seed(b"flag{demo}", seed)
                guess, plain = brute_seed(cipher, b"flag{", seed - 5, seed + 5)
                print("seed =", guess)
                print("plain =", plain)
            """
        ).strip()
        + "\n",
    },
    {
        "folder": "11_数学数论",
        "title": "数学数论",
        "summary": "很多 Crypto 题表面像算法，底层其实就是模运算、逆元、CRT、DLP、二次剩余这些数论工具题。",
        "background": "这类题的关键不是记住所有定理，而是看到数据就能把问题翻译成数学形式：同余方程、离散对数、平方剩余、连分数、多项式模运算等。",
        "when_to_think": [
            "题目一直在写同余、模方程、群阶、离散对数、平方根、连分数、递推。",
            "没有明显的标准密码名，但数据全是整数关系和模运算。",
            "题目要求解 `a*x ≡ 1 (mod m)`、`x^2 ≡ a (mod p)`、`g^x ≡ h (mod p)`。",
            "出现 `CRT`、`Pohlig-Hellman`、`Tonelli-Shanks`、`Legendre`、`Pell` 等术语。",
        ],
        "data_signals": [
            "多个模方程同时出现，优先想到 CRT。",
            "求逆元、约分失败、分母在模意义下怎么处理，都是逆元信号。",
            "离散对数、`p-1` 光滑、群阶分解，说明要做 DLP/PH/BSGS。",
            "矩阵递推、GF(2)、多项式模运算，常见于 LFSR、NTRU、CRC。",
        ],
        "subtypes": [
            "模逆元、CRT",
            "离散对数、BSGS、Pohlig-Hellman",
            "二次剩余、Legendre 符号",
            "Pell 方程、连分数、多项式模运算、矩阵快速幂",
        ],
        "starter_steps": [
            "先把题目口语化描述翻成精确方程。",
            "如果涉及除法，先问自己在模意义下是不是要求逆元。",
            "如果有多个模方程，优先用 CRT 合并，看是否能降维。",
            "如果题目规模中等，BSGS/矩阵快速幂往往是很好用的中间武器。",
        ],
        "pitfalls": [
            "模运算里不能直接做普通除法，必须乘逆元。",
            "不是每个元素都有逆元，先看 gcd 是否为 1。",
            "看起来是 RSA/ECC 的题，有时核心其实只是其中一个数论子问题。",
        ],
        "script_focus": "脚本给出逆元和 CRT 的纯 Python 模板，这两个在刷题里出场率非常高。",
        "example_code": dedent(
            """
            def egcd(a: int, b: int) -> tuple[int, int, int]:
                if b == 0:
                    return a, 1, 0
                g, x1, y1 = egcd(b, a % b)
                return g, y1, x1 - (a // b) * y1


            def inverse(a: int, m: int) -> int:
                g, x, _ = egcd(a, m)
                if g != 1:
                    raise ValueError("inverse does not exist")
                return x % m


            def crt(remainders: list[int], moduli: list[int]) -> int:
                x = 0
                M = 1
                for m in moduli:
                    M *= m
                for a, m in zip(remainders, moduli):
                    Mi = M // m
                    x += a * Mi * inverse(Mi, m)
                return x % M


            if __name__ == "__main__":
                print("inverse(3, 11) =", inverse(3, 11))
                print("crt =", crt([2, 3, 2], [3, 5, 7]))
            """
        ).strip()
        + "\n",
    },
    {
        "folder": "12_协议类",
        "title": "协议类",
        "summary": "考点常出现在密钥交换、身份认证、参数协商和签名验证流程里，重点是看协议有没有把密码学原语用对。",
        "background": "协议题表面上参数很多，但本质上还是那几种错误：群参数选坏了、没有认证、中间人、把公钥换成弱值、或者直接允许你传危险边界值。",
        "when_to_think": [
            "题目给 `p, g, A, B`、`session`、`token`、`JWT`、`cookie`、认证流程或握手过程。",
            "需要你模拟客户端/服务端交互，而不是单纯解一串密文。",
            "题目强调 `DH`、`SRP`、`JWT`、`RS256/HS256`、区块链签名。",
            "服务端让你提交公钥、nonce、共享参数或签名材料。",
        ],
        "data_signals": [
            "`p, g, A, B` 基本直指 Diffie-Hellman。",
            "`alg=none`、`RS256` 改 `HS256`、弱 secret，常见 JWT 伪造。",
            "`A = 0`、`g = 1 / p-1` 之类边界输入是在暗示协议参数没做检查。",
            "如果协议层里又嵌了 ECDSA/RSA，注意组合漏洞而不是只盯底层算法。",
        ],
        "subtypes": [
            "Diffie-Hellman 基础与弱参数",
            "MITM、中间值替换、认证缺失",
            "SRP 弱参数",
            "JWT / Cookie 签名伪造、区块链签名恢复",
        ],
        "starter_steps": [
            "先画出参与方、消息流、每一步用到的参数。",
            "判断问题是“数学可解”还是“协议没做校验”。",
            "检查群参数和边界输入：`g`、`A`、`B`、子群阶、认证步骤。",
            "如果是 token/cookie，先分清签名算法，再看是否能伪造或降级。",
        ],
        "pitfalls": [
            "很多协议题真正破的是流程，不是底层数学。",
            "只看到 DH 不够，要继续问：`g` 有没有问题？有没有认证？",
            "JWT 看起来像 Web 题，但本质上确实在考 Crypto 使用错误。",
        ],
        "script_focus": "脚本用一个小规模 DH 例子演示共享密钥计算和暴力离散对数，方便你快速定位协议题的数学部分。",
        "example_code": dedent(
            """
            def baby_dlog(g: int, h: int, p: int) -> int | None:
                cur = 1
                for x in range(p):
                    if cur == h:
                        return x
                    cur = (cur * g) % p
                return None


            if __name__ == "__main__":
                p, g = 467, 2
                a = 31
                A = pow(g, a, p)
                b = 57
                B = pow(g, b, p)
                shared = pow(B, a, p)
                recovered_a = baby_dlog(g, A, p)
                print("shared =", shared)
                print("recovered a =", recovered_a)
            """
        ).strip()
        + "\n",
    },
    {
        "folder": "13_签名算法",
        "title": "签名算法",
        "summary": "重点是识别 nonce、padding、验证规则是否安全，而不是“怎么把签名算法算一遍”。",
        "background": "签名题最常见的高价值漏洞就是 nonce 重用、nonce 部分泄露、验证逻辑过宽、签名可塑性或 RSA 低指数伪造。",
        "when_to_think": [
            "题目给出签名 `(r, s)`、消息摘要、公钥参数，或者让你伪造签名。",
            "出现 `ECDSA`、`DSA`、`Schnorr`、`RSA signature`、`nonce`。",
            "同一个公钥对多条消息签名，其中某些字段重复。",
            "服务端会验证签名而不是解密密文。",
        ],
        "data_signals": [
            "两个签名的 `r` 相同，优先想到 nonce 重用。",
            "给 `k` 的部分比特、`nonce bias`、`partial leakage`，优先想到 HNP 或格。",
            "RSA 签名题若 `e` 很小且 padding 检查松，可能可伪造。",
            "某些签名允许 `(r, n-s)` 也合法，说明存在可塑性。",
        ],
        "subtypes": [
            "DSA/ECDSA nonce 重用",
            "nonce 部分泄露",
            "Schnorr nonce 问题",
            "RSA 签名伪造、签名可塑性",
        ],
        "starter_steps": [
            "先检查多组签名里有没有重复的 `r`、相同的消息或相近的 nonce。",
            "写出签名方程，确认未知量是 `k` 还是私钥 `x`。",
            "如果是 RSA 签名，先看 padding 验证是否严格、`e` 是否很小。",
            "交互题要测试验证器是不是过于宽松。",
        ],
        "pitfalls": [
            "签名题里最容易漏看的就是“相同 `r`”，一定要先扫一遍。",
            "消息哈希 `h` 的取法要和题目保持一致，别把原文直接代入公式。",
            "如果题目是 Schnorr/EdDSA，公式和 ECDSA 不完全一样，别机械套用。",
        ],
        "script_focus": "脚本用 DSA/ECDSA 的 nonce 重用公式恢复 `k` 和私钥，是最值得背熟的一套模板。",
        "example_code": dedent(
            """
            def inverse(a: int, n: int) -> int:
                return pow(a, -1, n)


            def recover_nonce_and_key(h1: int, h2: int, s1: int, s2: int, r: int, q: int):
                k = ((h1 - h2) * inverse((s1 - s2) % q, q)) % q
                x = ((s1 * k - h1) * inverse(r, q)) % q
                return k, x


            if __name__ == "__main__":
                q = 101
                x = 17
                k = 29
                r = 37
                h1, h2 = 12, 44
                s1 = ((h1 + x * r) * inverse(k, q)) % q
                s2 = ((h2 + x * r) * inverse(k, q)) % q
                print(recover_nonce_and_key(h1, h2, s1, s2, r, q))
            """
        ).strip()
        + "\n",
    },
    {
        "folder": "14_Padding",
        "title": "Padding",
        "summary": "Padding 本身不是算法，但它经常成为 AES-CBC、RSA PKCS#1 v1.5 这类题真正能打进去的缺口。",
        "background": "很多选手一看到 AES 或 RSA 就紧张，其实真正能利用的是服务端如何处理 padding：是补位值、错误提示、长度检查，还是 oracle 回显。",
        "when_to_think": [
            "题目出现 `padding`、`PKCS#7`、`PKCS#1 v1.5`、`OAEP`、`oracle`。",
            "服务端返回“padding error”“invalid block type”“解密失败”等不同错误。",
            "AES-CBC 解密后会验证填充，RSA 会验证块格式。",
            "允许你不断提交修改后的密文并观察结果差异。",
        ],
        "data_signals": [
            "CBC 解密后明文末尾看起来像 `05 05 05 05 05`，这就是 PKCS#7。",
            "RSA 明文块以 `00 02` 或 `00 01` 开头，涉及 PKCS#1 v1.5。",
            "如果只要区分“padding 对/错”，就足够构造 padding oracle。",
            "OAEP 一旦随机数固定或校验顺序出错，也可能变成漏洞题。",
        ],
        "subtypes": [
            "PKCS#7 Padding",
            "CBC Padding Oracle",
            "PKCS#1 v1.5、Bleichenbacher 风格问题",
            "OAEP 使用错误",
        ],
        "starter_steps": [
            "先确认是哪一种 padding 规则，再复现本地校验逻辑。",
            "如果能交互，优先测试不同错误信息是否可区分。",
            "CBC 题里先理清“改前一块影响后一块明文”的关系。",
            "RSA 题里要关注块头格式和验证是否严格。",
        ],
        "pitfalls": [
            "Padding oracle 的关键不是拿到明文，而是能否区分有效/无效 padding。",
            "PKCS#7 不是随便补零，补位值必须等于补位长度。",
            "很多题名里不写 padding，但错误信息已经把答案送到你脸上了。",
        ],
        "script_focus": "脚本演示 PKCS#7 的补位与去补位逻辑，方便你先本地验证 padding 是否正确。",
        "example_code": dedent(
            """
            def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
                pad_len = block_size - (len(data) % block_size)
                return data + bytes([pad_len]) * pad_len


            def pkcs7_unpad(data: bytes, block_size: int = 16) -> bytes:
                if not data or len(data) % block_size != 0:
                    raise ValueError("bad length")
                pad_len = data[-1]
                if pad_len == 0 or pad_len > block_size:
                    raise ValueError("bad padding value")
                if data[-pad_len:] != bytes([pad_len]) * pad_len:
                    raise ValueError("bad padding bytes")
                return data[:-pad_len]


            if __name__ == "__main__":
                padded = pkcs7_pad(b"flag")
                print(padded)
                print(pkcs7_unpad(padded))
            """
        ).strip()
        + "\n",
    },
    {
        "folder": "15_图片音频文件混合Crypto",
        "title": "图片 / 音频 / 文件混合 Crypto",
        "summary": "题目载体看起来像 Misc，但真正突破点在于你需要先从媒体里抽出可被 Crypto 处理的数据。",
        "background": "这类题的难点通常在“提取”而不是“解密”。你要先把像素、二维码、频谱、隐藏文本、字体差异这些线索变成 bit、hex、base64 或可打印文本，再进入正常 Crypto 流程。",
        "when_to_think": [
            "附件是图片、音频、Word、PDF，而不是直接给你密文。",
            "题目提示黑白像素、RGB 奇偶、二维码、频谱、批注、隐藏对象、白色文字。",
            "提取出的结果看起来像 0/1、A/B、Base64、Hex、Morse。",
            "题目名在 Misc 和 Crypto 边界反复暗示你“先取数据，再解密”。",
        ],
        "data_signals": [
            "黑白像素、两种字体、两种颜色，非常像 Bacon / Binary 载体。",
            "音频滴滴声和长短音，优先想到 Morse。",
            "二维码、条码、元数据里常藏下一层 key 或密文。",
            "文档里白色文字、批注、对象层级差异，往往是隐藏密文入口。",
        ],
        "subtypes": [
            "图片像素转二进制",
            "二维码提取后再做 Base/AES/RSA",
            "音频摩斯密码、频谱图隐藏密文",
            "Word / PDF 隐藏文本、字体差异表示 0/1",
        ],
        "starter_steps": [
            "先判断载体里藏的是比特、字符还是另一层文件。",
            "能拿到 0/1、A/B、点横后，再按 Binary/Bacon/Morse/ASCII 思路继续。",
            "对图片先看像素、通道奇偶、二维码；对音频先看波形和频谱；对文档先看隐藏层和批注。",
            "提取出的中间结果要及时保存，不要每次都从载体重新做。",
        ],
        "pitfalls": [
            "别把这类题只当 Misc，因为提取出来之后经常还套着标准 Crypto。",
            "图片里两种颜色不一定是 LSB，也可能只是 Bacon 映射。",
            "提取结果像乱码时，先想编码问题，不要马上怀疑自己提取错了。",
        ],
        "script_focus": "脚本从一串 0/1 bit 流恢复 bytes 和 ASCII，适合作为图片/文档提取后的第二步模板。",
        "example_code": dedent(
            """
            def bits_to_bytes(bits: str) -> bytes:
                bits = bits.replace(" ", "").replace("\\n", "")
                if len(bits) % 8 != 0:
                    raise ValueError("bit length must be a multiple of 8")
                return bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))


            def bytes_to_ascii(data: bytes) -> str:
                return data.decode(errors="replace")


            if __name__ == "__main__":
                bits = "01100110 01101100 01100001 01100111"
                raw = bits_to_bytes(bits)
                print(raw)
                print(bytes_to_ascii(raw))
            """
        ).strip()
        + "\n",
    },
    {
        "folder": "16_自定义密码",
        "title": "自定义密码算法",
        "summary": "作者自己写的加密往往不安全，关键是把每一步拆开，看它到底是线性的、可逆的、可枚举的，还是能转成方程。",
        "background": "CTF 里大量“自创加密”只是把异或、加减、移位、矩阵、置换、shuffle 缝在一起。别被代码长度吓住，核心是判断每一步能不能单独逆掉。",
        "when_to_think": [
            "附件直接给了 Python/C 源码，里面自己写了 `encrypt()`。",
            "题目没有标准算法名，只有很多位运算、数组下标、交换、矩阵和循环。",
            "看起来“很复杂”，但每一步都只是加减异或移位这些便宜操作。",
            "输出和输入长度差不多，且流程完全可读、可模拟。",
        ],
        "data_signals": [
            "`x = ((x ^ k) + a) & 0xff` 这种式子通常可逐步逆推。",
            "`perm[i]`、`shuffle`、`swap` 提示是置换/打乱问题。",
            "矩阵乘法 mod 26 或 mod 256，说明可能能做逆矩阵。",
            "大量 xor 方程常可转成 GF(2) 线性系统。",
        ],
        "subtypes": [
            "线性加密、可逆运算逆推",
            "随机打乱、置换加密",
            "矩阵加密、Hill 密码",
            "GF(2) 线性系统、SAT/SMT 求解",
        ],
        "starter_steps": [
            "先把加密过程按步骤抄出来，标明每一步输入输出。",
            "判断每一步是否可逆：加减、异或、循环移位、置换基本都能逆。",
            "如果有 shuffle/perm，优先求逆置换。",
            "如果逻辑太绕，试着把条件写进 Z3 或线性方程组。",
        ],
        "pitfalls": [
            "不要看到自定义算法就慌，很多时候它比标准密码简单得多。",
            "逆运算顺序必须和加密顺序完全反过来。",
            "代码里如果混了字符编码、取模、位宽截断，要同步处理，不然很容易差一个字节。",
        ],
        "script_focus": "脚本演示如何逆掉一串加减异或和置换操作，是处理自定义加密最常见的骨架。",
        "example_code": dedent(
            """
            def encrypt_byte(x: int, k: int, a: int) -> int:
                return ((x ^ k) + a) & 0xFF


            def decrypt_byte(y: int, k: int, a: int) -> int:
                return ((y - a) & 0xFF) ^ k


            def invert_permutation(perm: list[int]) -> list[int]:
                inv = [0] * len(perm)
                for i, p in enumerate(perm):
                    inv[p] = i
                return inv


            if __name__ == "__main__":
                value = encrypt_byte(0x66, 0x12, 7)
                print(hex(value), hex(decrypt_byte(value, 0x12, 7)))
                perm = [2, 0, 1]
                print("inverse perm =", invert_permutation(perm))
            """
        ).strip()
        + "\n",
    },
    {
        "folder": "17_脑洞类Crypto",
        "title": "脑洞类 Crypto",
        "summary": "这类题不一定强依赖数学，而是把提示藏在标题、文件名、排版、首字母、藏头等地方。",
        "background": "脑洞题看起来不“正经”，但它们经常是整道题的破局点。你真正要学的是观察题目外观和上下文，而不是只盯密文本身。",
        "when_to_think": [
            "题目数据并不复杂，但怎么解都不顺，反而题名、文件名、段落格式很可疑。",
            "文字材料很多，像诗、句子、注释、对话、目录，而不是参数表。",
            "题目名像 `Caesar's secret`、`easy_RSA`、`baby_lfsr` 这种直接带提示。",
            "flag 解出来不像完整字符串，可能还需要套格式或继续拼接。",
        ],
        "data_signals": [
            "每行首字、每词首字母可能组成信息。",
            "高频字母、词频统计可能提示替换关系。",
            "题目标题、附件名、路径名本身就是提示。",
            "题面里强调某个大小写、换行、标点或排版，通常不是废话。",
        ],
        "subtypes": [
            "诗词藏头、首字母密码",
            "词频 / 字频提示",
            "题目标题藏提示、文件名提示",
            "flag 格式提示",
        ],
        "starter_steps": [
            "先看题目名字、附件名、注释和排版，再看密文本身。",
            "尝试提取每行首字、每个单词首字母、每段固定位置字符。",
            "如果像英文替换题，先做简单词频统计。",
            "如果你只解出了核心内容，记得补上题目要求的 flag 格式。",
        ],
        "pitfalls": [
            "脑洞不等于乱猜，依然要从题面中找可验证的规律。",
            "不要忽略附件名和目录名，它们经常就是最直白的提示。",
            "很多脑洞题最后还是会落回编码、古典密码或 XOR 上。",
        ],
        "script_focus": "脚本演示提取藏头和首字母，适合快速排查“题面本身就在说话”的题。",
        "example_code": dedent(
            """
            def acrostic(lines: list[str]) -> str:
                return "".join(line[0] for line in lines if line)


            def initials(text: str) -> str:
                return "".join(word[0] for word in text.split() if word)


            if __name__ == "__main__":
                poem = ["风起青萍", "落日长河", "安知我意", "歌尽桃花"]
                print("藏头 =", acrostic(poem))
                print("首字母 =", initials("For Love And Glory"))
            """
        ).strip()
        + "\n",
    },
    {
        "folder": "18_组合套娃",
        "title": "组合套娃",
        "summary": "比赛里很少只考一层，真正高频的是多种简单方法串联：先提取，再解码，再做 XOR 或 AES。",
        "background": "套娃题的核心不是学会某个新算法，而是保持分层意识。每解开一层都重新观察数据，不要因为第一层很简单就漏掉后面的真正考点。",
        "when_to_think": [
            "你解完一层之后，结果看起来仍然很像另一种编码或密文。",
            "题目素材跨越图片、文本、脚本和参数文件，不像单一算法。",
            "作者刻意把 `base64`、`hex`、`xor`、`AES`、`RSA` 这类多种线索混在一起。",
            "中间结果不是 flag，但明显是下一层算法的合法输入。",
        ],
        "data_signals": [
            "常见链路如 `hex -> ascii -> caesar`、`base64 -> xor`、`RSA -> AES key`。",
            "媒体提取出的 0/1 或二维码内容，往往只是进入下一层的门票。",
            "如果中间结果像 key、iv、nonce、公钥，那通常说明下一层是现代密码。",
            "每层输出都要检查：是文本？字节？整数？文件头？",
        ],
        "subtypes": [
            "编码 + 古典密码",
            "编码 + XOR",
            "图片/音频提取 + 编码/古典密码",
            "RSA 解 key + 对称解密",
            "随机数预测 + 恢复流密码 key",
        ],
        "starter_steps": [
            "每过一层都保存结果，并记录“这一层用了什么、为什么判断是它”。",
            "不要一次写死整条链，先让每层都能单独验证。",
            "如果中间结果变成大整数、参数组或固定长度块，立刻重新分类题型。",
            "套娃题很吃耐心，别因为第一层简单就放松观察。",
        ],
        "pitfalls": [
            "最大的坑是解开第一层就以为结束了。",
            "每层的数据类型不同，字符串、字节、整数转换很容易出错。",
            "中间结果像乱码不代表错，可能只是下一层的原始密文。",
        ],
        "script_focus": "脚本给出一个“多阶段处理”的骨架，示例链路是 Hex -> Base64 -> XOR，方便你改成自己的套娃流程。",
        "example_code": dedent(
            """
            import base64


            def repeating_key_xor(cipher: bytes, key: bytes) -> bytes:
                return bytes(cipher[i] ^ key[i % len(key)] for i in range(len(cipher)))


            def pipeline(data: str) -> bytes:
                stage1 = bytes.fromhex(data)
                stage2 = base64.b64decode(stage1)
                stage3 = repeating_key_xor(stage2, b"key")
                return stage3


            if __name__ == "__main__":
                sample = base64.b64encode(bytes([ord("f") ^ ord("k")]))
                wrapped = sample.hex()
                print(pipeline(wrapped))
            """
        ).strip()
        + "\n",
    },
]


def make_markdown(topic: dict[str, object]) -> str:
    title = topic["title"]
    summary = topic["summary"]
    background = topic["background"]
    script_focus = topic["script_focus"]
    lines = [
        f"# {title}",
        "",
        f"这份资料基于 `{SOURCE_FILE}` 中的《CTF Crypto 常见题型总结》整理，并强化成“看到什么数据/提示时该想到什么题型”的速查笔记。",
        "",
        "## 题型表述",
        "",
        str(summary),
        "",
        "## 背景",
        "",
        str(background),
        "",
        "## 什么时候该想到这类题",
        "",
    ]
    lines.extend(f"- {item}" for item in topic["when_to_think"])
    lines.extend(
        [
            "",
            "## 题目里出现这些数据或提示时，优先联想到它",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in topic["data_signals"])
    lines.extend(
        [
            "",
            "## 这一类常见子题",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in topic["subtypes"])
    lines.extend(
        [
            "",
            "## 实战里建议怎么入手",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in topic["starter_steps"])
    lines.extend(
        [
            "",
            "## 常见误区",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in topic["pitfalls"])
    lines.extend(
        [
            "",
            "## 配套示例脚本说明",
            "",
            str(script_focus),
            "",
            "`example.py` 不是通杀脚本，而是一个可对照改写的起手模板。你遇到同类题时，先把题目的输入格式、参数名和题面条件替换进去，再继续扩展。",
        ]
    )
    return "\n".join(lines) + "\n"


def make_index(topics: list[dict[str, object]]) -> str:
    lines = [
        "# CTF Crypto 题型资料包",
        "",
        f"整理来源：`{SOURCE_FILE}`",
        "",
        "这个目录按“大题型”拆分，每个题型文件夹里都有两份内容：",
        "",
        "- `README.md`：讲清楚这类题的表述、背景、识别信号、什么时候该想到它。",
        "- `example.py`：放一个可以直接对照改写的最小脚本骨架。",
        "",
        "## 目录",
        "",
    ]
    for topic in topics:
        folder = topic["folder"]
        title = topic["title"]
        summary = topic["summary"]
        lines.append(f"- `{folder}`：{title}。{summary}")
    lines.extend(
        [
            "",
            "## 建议使用方式",
            "",
            "- 先根据题目数据特征去对应目录找题型，不要上来就盲搜脚本。",
            "- 先看 `README.md` 判断方向，再用 `example.py` 改成适合当前题目的版本。",
            "- 如果一道题明显有多层，优先再看 `18_组合套娃`，把每一层拆开做。",
            "- RSA、ECC、随机数、签名这几类题，最重要的是先确认“漏洞点”而不是先写代码。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "00_总索引.md").write_text(make_index(TOPICS), encoding="utf-8")

    for topic in TOPICS:
        topic_dir = OUTPUT_DIR / str(topic["folder"])
        topic_dir.mkdir(parents=True, exist_ok=True)
        (topic_dir / "README.md").write_text(make_markdown(topic), encoding="utf-8")
        (topic_dir / "example.py").write_text(str(topic["example_code"]), encoding="utf-8")

    print(f"generated {len(TOPICS)} topic folders under {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

# def generate_segment_mask(segment_map, active_level):
#     """
#     根据段码映射和有效电平生成数码管显示的段码掩码（支持任意字符）
#
#     :param segment_map: 段码映射字符串，如 "a1b2c3d4e5f6g7dp0"
#     :param active_level: 有效电平（1或0），1表示bit=1时段亮，0表示bit=0时段亮
#     :return: 返回一个字典，键为字符（数字/字母），值为对应的段码掩码（8位无符号整数）
#     """
#     # 包含字母的完整段码表
#     segment_table = {
#         # 数字部分
#         0: [1, 1, 1, 1, 1, 1, 0, 0], 1: [0, 1, 1, 0, 0, 0, 0, 0],
#         2: [1, 1, 0, 1, 1, 0, 1, 0], 3: [1, 1, 1, 1, 0, 0, 1, 0],
#         4: [0, 1, 1, 0, 0, 1, 1, 0], 5: [1, 0, 1, 1, 0, 1, 1, 0],
#         6: [1, 0, 1, 1, 1, 1, 1, 0], 7: [1, 1, 1, 0, 0, 0, 0, 0],
#         8: [1, 1, 1, 1, 1, 1, 1, 0], 9: [1, 1, 1, 1, 0, 1, 1, 0],
#
#         # 大写字母
#         'A': [1, 1, 0, 1, 1, 1, 1, 0],
#         'C': [1, 0, 0, 1, 1, 1, 0, 0],
#         'E': [1, 0, 0, 1, 1, 1, 1, 0],
#         'F': [1, 0, 0, 0, 1, 1, 1, 0],
#         'G': [0, 1, 1, 1, 1, 1, 0, 0],
#         'H': [0, 1, 1, 0, 1, 1, 1, 0],
#         'I': [0, 1, 1, 0, 0, 0, 0, 0],
#         'J': [0, 1, 1, 1, 1, 0, 0, 0],
#         'L': [0, 0, 0, 1, 1, 1, 0, 0],
#         'O': [1, 1, 1, 1, 1, 1, 0, 0],
#         'P': [1, 1, 0, 0, 1, 1, 1, 0],
#         'S': [1, 0, 1, 1, 0, 1, 1, 0],
#         'U': [0, 1, 1, 1, 1, 1, 0, 0],
#
#         # 小写字母
#         'b': [0, 0, 1, 1, 1, 1, 1, 0],
#         'c': [0, 0, 1, 1, 0, 0, 1, 0],
#         'd': [1, 1, 1, 1, 0, 0, 1, 0],
#         'g': [1, 1, 1, 1, 0, 1, 1, 0],
#         'h': [0, 0, 1, 0, 1, 1, 1, 0],
#         'i': [0, 0, 1, 0, 0, 0, 0, 0],
#         'l': [0, 1, 1, 0, 0, 0, 0, 0],
#         'n': [0, 0, 1, 0, 1, 0, 1, 0],
#         'o': [0, 0, 1, 1, 1, 0, 1, 0],
#         'q': [1, 1, 1, 0, 0, 1, 1, 0],
#         'r': [0, 0, 0, 0, 1, 0, 1, 0],
#         't': [0, 0, 0, 1, 1, 1, 1, 0],
#         'u': [0, 0, 1, 1, 1, 0, 0, 0],
#
#         # 特殊字符
#         '-': [0, 0, 0, 0, 0, 0, 0, 1]
#     }
#
#     # 解析段码映射字符串（如 "a1b2c3d4e5f6g7dp0"）
#     segment_to_bit = {}
#     i = 0
#     while i < len(segment_map):
#         # 检查当前字符是否是字母
#         if segment_map[i].isalpha():
#             # 如果是 'd'，检查下一个字符是否是 'p'（处理 dp 情况）
#             if segment_map[i] == 'd' and i + 1 < len(segment_map) and segment_map[i + 1] == 'p':
#                 segment = 'dp'
#                 i += 2  # 跳过 'd' 和 'p'
#             else:
#                 segment = segment_map[i]
#                 i += 1  # 跳过字母
#             # 读取数字部分
#             if i < len(segment_map) and segment_map[i].isdigit():
#                 bit = int(segment_map[i])
#                 segment_to_bit[segment] = bit
#                 i += 1  # 跳过数字
#             else:
#                 raise ValueError(f"Invalid segment map format: missing bit number after '{segment}'")
#         else:
#             raise ValueError(f"Invalid segment map format: expected letter at position {i}")
#
#     # 生成所有字符的段码掩码
#     mask_dict = {}
#     for char in segment_table:  # 关键修改：遍历所有字符
#         mask = 0x00
#         for segment, bit in segment_to_bit.items():
#             # 获取段位置
#             if segment == 'dp':
#                 seg_idx = 7
#             else:
#                 seg_idx = ord(segment) - ord('a')
#
#             # 获取段状态（处理字母）
#             try:
#                 segment_state = segment_table[char][seg_idx]
#             except IndexError:
#                 raise ValueError(f"字符 {char} 的段码定义不完整")
#
#             # 计算有效电平
#             if active_level == 0:
#                 segment_state = 1 - segment_state
#
#             # 设置bit位
#             if segment_state:
#                 mask |= (1 << bit)
#
#         mask_dict[char] = mask
#
#     return mask_dict, segment_to_bit
#
#
# # # # 示例：共阴数码管（高电平有效）
# # # segment_map = "e4d5dp2c6g7a1f0b3"
# # # active_level = 1
# # # mask_dict = generate_segment_mask(segment_map, active_level)
# # #
# # # # 打印所有字符的段码
# # # for char, mask in mask_dict.items():
# # #     print(f"字符 '{char}': 段码 = 0x{mask:02X}")
# #
# # segment_map = "e4d5dp2c6g7a1f0b3"
# # active_level = 1
# #
# # mask_dict = generate_segment_mask(segment_map, active_level)
# #
# # # 数字部分 (0-9)
# # num_labels = [f"{num:>4}" for num in range(10)]
# # num_codes = [f"0x{mask_dict[num]:02X}" for num in range(10)]
# #
# # # 字母部分 (A-Z)
# # letter_items = sorted([(char, mask_dict[char]) for char in mask_dict if isinstance(char, str) and char.isalpha()], key=lambda x: x[0])
# # letter_labels = [f"{char:>4}" for char, _ in letter_items]
# # letter_codes = [f"0x{code:02X}" for _, code in letter_items]
# #
# # # 格式输出
# # print("依次对应的是：[{}]".format(", ".join(num_labels)))
# # print("数字段码数组：[{}]".format(", ".join(num_codes)))
# # print("\n依次对应的是：[{}]".format(", ".join(letter_labels)))
# # print("字母段码数组：[{}]".format(", ".join(letter_codes)))
#
#
#
#
# # 示例调用
# segment_map = "e4d5dp2c6g7a1f0b3"
# active_level = 1
#
# # 获取段码字典和映射关系
# mask_dict, segment_to_bit = generate_segment_mask(segment_map, active_level)
#
# # 获取DP位位置
# dp_bit = segment_to_bit.get('dp', None)
# if dp_bit is None:
#     raise ValueError("段码映射中未定义dp位")
#
# # 生成常规数字段码
# num_labels = [f"{num:>4}" for num in range(10)]
# num_codes = [f"0x{mask_dict[num]:02X}" for num in range(10)]
#
# # 生成带DP位的数字段码
# num_codes_with_dp = [f"0x{(mask_dict[num] | (1 << dp_bit)):02X}" for num in range(10)]
#
# # 生成字母段码
# letter_items = sorted([(char, mask_dict[char])
#                       for char in mask_dict
#                       if isinstance(char, str) and char.isalpha()],
#                      key=lambda x: x[0])
# letter_labels = [f"{char:>4}" for char, _ in letter_items]
# letter_codes = [f"0x{code:02X}" for _, code in letter_items]
#
# # 格式化输出
# print("依次对应的是：[{}]".format(", ".join(num_labels)))
# print("数字段码数组：[{}]".format(", ".join(num_codes)))
# print("\n依次对应的是：[{}]".format(", ".join(num_labels)))
# print("数字段码数组：[{}]".format(", ".join(num_codes_with_dp)),"（DP位强制为1）")
# print("\n依次对应的是：[{}]".format(", ".join(letter_labels)))
# print("字母段码数组：[{}]".format(", ".join(letter_codes)))

def generate_segment_mask(segment_map, active_level):
    """
    根据段码映射和有效电平生成数码管显示的段码掩码（支持任意字符）

    :param segment_map: 段码映射字符串，如 "a1b2c3d4e5f6g7dp0"
    :param active_level: 有效电平（1或0），1表示bit=1时段亮，0表示bit=0时段亮
    :return: 返回一个字典，键为字符（数字/字母），值为对应的段码掩码（8位无符号整数）
    """
    # 包含字母的完整段码表
    segment_table = {
        0: [1, 1, 1, 1, 1, 1, 0, 0], 1: [0, 1, 1, 0, 0, 0, 0, 0],
        2: [1, 1, 0, 1, 1, 0, 1, 0], 3: [1, 1, 1, 1, 0, 0, 1, 0],
        4: [0, 1, 1, 0, 0, 1, 1, 0], 5: [1, 0, 1, 1, 0, 1, 1, 0],
        6: [1, 0, 1, 1, 1, 1, 1, 0], 7: [1, 1, 1, 0, 0, 0, 0, 0],
        8: [1, 1, 1, 1, 1, 1, 1, 0], 9: [1, 1, 1, 1, 0, 1, 1, 0],

        'A': [1, 1, 1, 0, 1, 1, 1, 0],
        'C': [1, 0, 0, 1, 1, 1, 0, 0],
        'E': [1, 0, 0, 1, 1, 1, 1, 0],
        'F': [1, 0, 0, 0, 1, 1, 1, 0],
        'G': [1, 0, 1, 1, 1, 1, 0, 0],
        'H': [0, 1, 1, 0, 1, 1, 1, 0],
        'I': [0, 1, 1, 0, 0, 0, 0, 0],
        'J': [0, 1, 1, 1, 1, 0, 0, 0],
        'L': [0, 0, 0, 1, 1, 1, 0, 0],
        'O': [1, 1, 1, 1, 1, 1, 0, 0],
        'P': [1, 1, 0, 0, 1, 1, 1, 0],
        'S': [1, 0, 1, 1, 0, 1, 1, 0],
        'U': [0, 1, 1, 1, 1, 1, 0, 0],


        'b': [0, 0, 1, 1, 1, 1, 1, 0],
        'c': [0, 0, 0, 1, 1, 0, 1, 0],
        'd': [0, 1, 1, 1, 1, 0, 1, 0],
        'g': [1, 1, 1, 1, 0, 1, 1, 0],
        'h': [0, 0, 1, 0, 1, 1, 1, 0],
        'i': [0, 0, 1, 0, 0, 0, 0, 0],
        'l': [0, 1, 1, 0, 0, 0, 0, 0],
        'n': [0, 0, 1, 0, 1, 0, 1, 0],
        'o': [0, 0, 1, 1, 1, 0, 1, 0],
        'q': [1, 1, 1, 0, 0, 1, 1, 0],
        'r': [0, 0, 0, 0, 1, 0, 1, 0],
        't': [0, 0, 0, 1, 1, 1, 1, 0],
        'u': [0, 0, 1, 1, 1, 0, 0, 0],

        '-': [0, 0, 0, 0, 0, 0, 1, 0]
    }

    # 解析段码映射字符串（如 "a1b2c3d4e5f6g7dp0"）
    segment_to_bit = {}
    i = 0
    while i < len(segment_map):
        # 检查当前字符是否是字母
        if segment_map[i].isalpha():
            # 如果是 'd'，检查下一个字符是否是 'p'（处理 dp 情况）
            if segment_map[i] == 'd' and i + 1 < len(segment_map) and segment_map[i + 1] == 'p':
                segment = 'dp'
                i += 2  # 跳过 'd' 和 'p'
            else:
                segment = segment_map[i]
                i += 1  # 跳过字母
            # 读取数字部分
            if i < len(segment_map) and segment_map[i].isdigit():
                bit = int(segment_map[i])
                segment_to_bit[segment] = bit
                i += 1  # 跳过数字
            else:
                raise ValueError(f"Invalid segment map format: missing bit number after '{segment}'")
        else:
            raise ValueError(f"Invalid segment map format: expected letter at position {i}")

    # 生成所有字符的段码掩码
    mask_dict = {}
    for char in segment_table:  # 关键修改：遍历所有字符
        mask = 0x00
        for segment, bit in segment_to_bit.items():
            # 获取段位置
            if segment == 'dp':
                seg_idx = 7
            else:
                seg_idx = ord(segment) - ord('a')

            # 获取段状态（处理字母）
            try:
                segment_state = segment_table[char][seg_idx]
            except IndexError:
                raise ValueError(f"字符 {char} 的段码定义不完整")

            # 计算有效电平
            if active_level == 0:
                segment_state = 1 - segment_state

            # 设置bit位
            if segment_state:
                mask |= (1 << bit)

        mask_dict[char] = mask

    return mask_dict, segment_to_bit


# 示例调用
segment_map = "e4d5dp2c6g7a1f0b3"
active_level = 1

# 获取段码字典和映射关系
mask_dict, segment_to_bit = generate_segment_mask(segment_map, active_level)

# 获取DP位位置
dp_bit = segment_to_bit.get('dp', None)
if dp_bit is None:
    raise ValueError("段码映射中未定义dp位")

# 生成常规数字段码
num_labels = [f"{num:>4}" for num in range(10)]
num_codes = [f"0x{mask_dict[num]:02X}" for num in range(10)]

# 生成带DP位的数字段码
num_codes_with_dp = [f"0x{(mask_dict[num] | (1 << dp_bit)):02X}" for num in range(10)]

# 生成字母段码（包含大写和小写）
letter_items = sorted([(char, mask_dict[char])
                      for char in mask_dict
                      if isinstance(char, str) and char.isalpha()],
                     key=lambda x: x[0])
letter_labels = [f"{char:>4}" for char, _ in letter_items]
letter_codes = [f"0x{code:02X}" for _, code in letter_items]

# 生成特殊字符段码
special_chars = [char for char in mask_dict if isinstance(char, str) and not char.isalpha()]
special_labels = [f"{char:>4}" for char in special_chars]
special_codes = [f"0x{mask_dict[char]:02X}" for char in special_chars]

# 格式化输出
print("依次对应的是：[{}]".format(", ".join(num_labels)))
print("数字段码数组：[{}]".format(", ".join(num_codes)))

print("\n依次对应的是：[{}]".format(", ".join(num_labels)))
print("数字段码数组：[{}]".format(", ".join(num_codes_with_dp)),"（DP位强制为1）")

print("\n依次对应的是：[{}]".format(", ".join(letter_labels)))
print("字母段码数组：[{}]".format(", ".join(letter_codes)))

print("\n依次对应的是：[{}]".format(", ".join(special_labels)))
print("特殊字符段码：[{}]".format(", ".join(special_codes)))

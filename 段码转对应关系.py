def reverse_generate_segment_mask(hex_codes, active_level=1):
    """
    根据0-9的十六进制段码反推段与bit位的对应关系
    输入格式: 逗号分隔的十六进制值，如 "0x7B,0x42,0x5D,0x79,0x49,0x6D,0x6F,0x40,0x7F,0x7D"
    输出格式: 类似 "e4d5dp2c6g7a1f0b3" 的段码映射字符串
    """
    # 解析输入的十六进制段码
    try:
        if isinstance(hex_codes, str):
            # 更严格的输入验证
            hex_list = []
            for h in hex_codes.split(','):
                h = h.strip()
                if not h.startswith('0x') or len(h) != 4:
                    raise ValueError(f"格式错误: '{h}' 不是有效的十六进制值")
                hex_list.append(int(h, 16))
        else:
            hex_list = [int(h, 16) for h in hex_codes]

        if len(hex_list) != 10:
            raise ValueError(f"必须提供10个十六进制段码（0-9），当前提供了{len(hex_list)}个")

    except Exception as e:
        print(f"输入解析错误: {e}")
        return None, None  # 返回两个None，表示失败

    # 数码管段的标准亮灭定义（数字0-9）
    standard_segments = {
        0: {'a', 'b', 'c', 'd', 'e', 'f'},
        1: {'b', 'c'},
        2: {'a', 'b', 'd', 'e', 'g'},
        3: {'a', 'b', 'c', 'd', 'g'},
        4: {'b', 'c', 'f', 'g'},
        5: {'a', 'c', 'd', 'f', 'g'},
        6: {'a', 'c', 'd', 'e', 'f', 'g'},
        7: {'a', 'b', 'c'},
        8: {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
        9: {'a', 'b', 'c', 'd', 'f', 'g'}
    }

    # 初始化段到bit位的映射
    segment_to_bit = {}

    # 步骤1: 分析每个bit位在所有数字中的出现模式
    bit_patterns = {}
    for bit_pos in range(8):
        pattern = []
        for digit in range(10):
            pattern.append(1 if hex_list[digit] & (1 << bit_pos) else 0)
        bit_patterns[bit_pos] = tuple(pattern)

    # 步骤2: 为每个段构建理想模式
    ideal_patterns = {}
    for seg in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'dp']:
        pattern = []
        for digit in range(10):
            pattern.append(1 if seg in standard_segments[digit] else 0)
        ideal_patterns[seg] = tuple(pattern)

    # 步骤3: 找到最佳匹配
    # 优先匹配a-g段，最后处理dp
    segments_to_map = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'dp']

    for seg in segments_to_map:
        best_bit = None
        best_similarity = -1

        for bit_pos in range(8):
            if bit_pos in segment_to_bit.values():
                continue  # 该bit已被映射

            # 计算相似度（匹配位数）
            similarity = sum(1 for a, b in zip(bit_patterns[bit_pos], ideal_patterns[seg]) if a == b)

            if similarity > best_similarity:
                best_similarity = similarity
                best_bit = bit_pos

        if best_bit is not None and best_similarity > 5:  # 设置阈值，确保匹配质量
            segment_to_bit[seg] = best_bit

    # 检查是否成功映射所有段
    required_segments = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'dp'}
    missing_segments = required_segments - set(segment_to_bit.keys())
    if missing_segments:
        print(f"警告: 未能映射所有段，缺少: {', '.join(missing_segments)}")
        # 尝试通过排除法映射剩余段
        for seg in missing_segments:
            available_bits = [bit for bit in range(8) if bit not in segment_to_bit.values()]
            if available_bits:
                segment_to_bit[seg] = available_bits[0]
                print(f"  自动映射: {seg} → bit{available_bits[0]}")

    # 生成输出字符串（按bit位升序排列）
    sorted_segments = sorted(segment_to_bit.items(), key=lambda x: x[1])
    result = ''.join(f"{seg}{bit}" for seg, bit in sorted_segments)

    return result, segment_to_bit  # 返回两个值：结果字符串和映射字典


if __name__ == "__main__":
    print("=== 数码管段码反推工具 ===")
    print("输入格式示例: 0x7B,0x42,0x5D,0x79,0x49,0x6D,0x6F,0x40,0x7F,0x7D")

    # 示例输入（数字0-9的段码）
    input_hex = input("\n请输入0-9的十六进制段码（逗号分隔）：\n")

    # 反推段码映射
    segment_map, segment_to_bit = reverse_generate_segment_mask(input_hex)

    if segment_map and segment_to_bit:
        print(f"\n✅ 反推结果：{segment_map}")
        print("\n段与bit位对应关系：")
        for seg, bit in sorted(segment_to_bit.items(), key=lambda x: x[1]):
            print(f"  - 段 {seg} → bit{bit}")
    else:
        print("\n❌ 反推失败，请检查输入格式是否正确。")
        print("  正确格式示例: 0x7B,0x42,0x5D,0x79,0x49,0x6D,0x6F,0x40,0x7F,0x7D")



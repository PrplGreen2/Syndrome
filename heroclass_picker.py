def words_to_decimal_batch_input():
    word_map = ["brainy", "hearty", "sneaky", "beastly", "crazy",
                "kabloom", "megagrow", "guardian", "smarty", "solar"]
    
    # Initialize all bits to 0
    bits = {word: '0' for word in word_map}

    print("Default settings (all 0s):")
    for word in word_map:
        print(f"{word}: 0")
    
    print("\nTo change values, type like this: brainy=1 sneaky=1 solar=1. ALWAYS keep the blank string at 0")
    print("Then press ENTER to proceed with those values.\n")
    user_input = input("Edit values: ").strip()

    if user_input:
        entries = user_input.split()
        for entry in entries:
            if '=' in entry:
                word, value = entry.split('=')
                word, value = word.strip(), value.strip()
                if word in bits and value in ('0', '1'):
                    bits[word] = value
                else:
                    print(f"Ignored invalid input: {entry}")

    # Create binary string based on updated bits
    binary_str = ''.join(bits[word] for word in word_map)
    decimal_value = int(binary_str, 2)

    print("\nFinal binary configuration:")
    for word in word_map:
        print(f"{word}: {bits[word]}")

    print(f"\nBinary number: {binary_str}")
    print(f"Decimal value: {decimal_value}")

# Run the function
words_to_decimal_batch_input()

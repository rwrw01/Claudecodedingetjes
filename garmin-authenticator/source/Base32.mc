// Base32 decoder for TOTP secret keys (RFC 4648)
// Decodes Base32-encoded strings to byte arrays

using Toybox.Lang;

module Base32 {

    // Base32 alphabet lookup: returns value 0-31 for valid chars, -1 for invalid
    function charValue(ch as Number) as Number {
        // A-Z = 0-25
        if (ch >= 65 && ch <= 90) {  // 'A' to 'Z'
            return ch - 65;
        }
        // a-z = 0-25 (lowercase support)
        if (ch >= 97 && ch <= 122) {  // 'a' to 'z'
            return ch - 97;
        }
        // 2-7 = 26-31
        if (ch >= 50 && ch <= 55) {  // '2' to '7'
            return ch - 50 + 26;
        }
        return -1;  // Invalid character (including '=' padding)
    }

    // Decode a Base32-encoded string to a byte array
    function decode(encoded as String) as Array<Number> {
        var result = new [0];
        var buffer = 0;
        var bitsLeft = 0;

        for (var i = 0; i < encoded.length(); i++) {
            var ch = encoded.toCharArray()[i].toNumber();

            // Skip padding and whitespace
            if (ch == 61 || ch == 32 || ch == 10 || ch == 13) {  // '=', space, \n, \r
                continue;
            }

            var val = charValue(ch);
            if (val < 0) {
                continue;  // Skip invalid characters
            }

            buffer = (buffer << 5) | val;
            bitsLeft += 5;

            if (bitsLeft >= 8) {
                bitsLeft -= 8;
                result.add((buffer >> bitsLeft) & 0xFF);
            }
        }

        return result;
    }
}
